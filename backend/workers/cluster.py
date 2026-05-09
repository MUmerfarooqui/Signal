import uuid
from dataclasses import dataclass

import hdbscan
import numpy as np


@dataclass
class Cluster:
    label: int
    event_ids: list[uuid.UUID]
    source_ids: list[str]
    texts: list[str]
    urls: list[str]


def cluster_events(events: list) -> list[Cluster]:
    """
    Run HDBSCAN over raw_event embeddings.
    Returns one Cluster per theme found. Noise points (label -1) are dropped.
    """
    if len(events) < 3:
        return []

    embeddings = np.array([e.embedding for e in events], dtype=np.float32)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=3,
        min_samples=1,
        metric="euclidean",
    )
    labels = clusterer.fit_predict(embeddings)

    buckets: dict[int, list] = {}
    for event, label in zip(events, labels):
        if label == -1:
            continue
        buckets.setdefault(label, []).append(event)

    clusters = []
    for label, evts in buckets.items():
        # Sort by proximity to centroid so top texts are most representative
        vecs = np.array([e.embedding for e in evts], dtype=np.float32)
        centroid = vecs.mean(axis=0)
        distances = np.linalg.norm(vecs - centroid, axis=1)
        order = np.argsort(distances)
        sorted_evts = [evts[i] for i in order]

        clusters.append(Cluster(
            label=label,
            event_ids=[e.id for e in sorted_evts],
            source_ids=[e.source_id for e in sorted_evts],
            texts=[e.content for e in sorted_evts],
            urls=[e.url or "" for e in sorted_evts],
        ))

    # Largest clusters first
    clusters.sort(key=lambda c: len(c.event_ids), reverse=True)
    return clusters


def summarize_clusters(clusters: list[Cluster], top_n: int = 5) -> list[dict]:
    """
    Convert clusters into plain dicts suitable for sending to Claude.
    Caps each cluster at top_n representative tickets to control token count.
    """
    summaries = []
    for i, cluster in enumerate(clusters):
        summaries.append({
            "cluster_index": i,
            "ticket_count": len(cluster.event_ids),
            "representative_tickets": [
                {
                    "source_id": sid,
                    "text": text[:500],  # truncate very long tickets
                    "url": url,
                }
                for sid, text, url in zip(
                    cluster.source_ids[:top_n],
                    cluster.texts[:top_n],
                    cluster.urls[:top_n],
                )
            ],
        })
    return summaries
