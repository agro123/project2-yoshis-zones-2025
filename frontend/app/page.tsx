import YoshisZonesGame from "@/components/yoshis-zones-game"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gradient-to-b from-green-50 to-red-50">
      <h1 className="text-4xl font-bold text-center mb-6 text-green-600">Yoshi&apos;s Zones</h1>
      <YoshisZonesGame />
    </main>
  )
}
