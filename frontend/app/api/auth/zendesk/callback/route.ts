import { NextRequest, NextResponse } from "next/server"

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function GET(req: NextRequest) {
  const { searchParams } = req.nextUrl
  const code = searchParams.get("code")
  const state = searchParams.get("state")
  const error = searchParams.get("error")

  if (error) {
    return NextResponse.redirect(new URL(`/connectors?error=${error}`, req.url))
  }

  if (!code || !state) {
    return NextResponse.redirect(new URL("/connectors?error=missing_params", req.url))
  }

  // Forward to backend callback
  const backendUrl = `${API_URL}/api/v1/connectors/zendesk/callback?code=${code}&state=${state}`
  return NextResponse.redirect(backendUrl)
}
