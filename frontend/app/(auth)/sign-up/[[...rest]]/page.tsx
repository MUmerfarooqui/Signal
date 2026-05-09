import { SignUp } from "@clerk/nextjs"

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white dark:bg-zinc-950">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">Signal</h1>
        <p className="mt-1 text-sm text-zinc-500">Product intelligence, delivered.</p>
      </div>
      <SignUp forceRedirectUrl="/onboarding" />
    </div>
  )
}
