import YoshisZonesGame from "@/components/yoshis-zones-game"

export default function Home() {
  return (
    <main
      className="flex min-h-screen flex-col items-center justify-center p-4 bg-cover bg-center"
      style={{ backgroundImage: 'url("/images/yoshi-background.jpg")' }}
    >
      <div className="w-full max-w-4xl bg-white/55 backdrop-blur-sm p-6 rounded-xl shadow-xl flex flex-col items-center">
        <h1 className="text-4xl font-bold text-center mb-6 text-green-600">Yoshi&apos;s Zones</h1>
        <YoshisZonesGame />
      </div>
    </main>
  )
}
