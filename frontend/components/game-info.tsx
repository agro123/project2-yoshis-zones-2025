import type { Difficulty, GameStatus } from "./yoshis-zones-game"

interface GameInfoProps {
  greenZones: number
  redZones: number
  isGreenTurn: boolean
  gameStatus: GameStatus
  difficulty: Difficulty
}

export default function GameInfo({ greenZones, redZones, isGreenTurn, gameStatus, difficulty }: GameInfoProps) {
  // Mapeo de dificultad a profundidad
  const difficultyDepth = {
    beginner: 2,
    amateur: 4,
    expert: 6,
  }

  // Determinar mensaje de estado del juego
  let statusMessage = ""
  if (gameStatus === "playing") {
    statusMessage = isGreenTurn ? "Turno de Yoshi verde (máquina)" : "Tu turno (Yoshi rojo)"
  } else if (gameStatus === "green-wins") {
    statusMessage = "¡Yoshi verde gana!"
  } else if (gameStatus === "red-wins") {
    statusMessage = "¡Has ganado!"
  } else {
    statusMessage = "¡Empate!"
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow-md w-full max-w-xs">
      <h2 className="text-xl font-bold mb-4 text-center">Estado del juego</h2>

      <div className="flex justify-between mb-4">
        <div className="text-center">
          <div className="w-12 h-12 mx-auto mb-2 flex items-center justify-center">
            <img src="/images/green-yoshi.png" alt="Green Yoshi" className="w-full h-full object-contain" />
          </div>
          <p className="font-medium">Yoshi verde (máquina)</p>
          <p className="text-2xl font-bold">{greenZones}</p>
        </div>

        <div className="text-center">
          <div className="w-12 h-12 mx-auto mb-2 flex items-center justify-center">
            <img src="/images/red-yoshi.png" alt="Red Yoshi" className="w-full h-full object-contain" />
          </div>
          <p className="font-medium">Yoshi rojo (tú)</p>
          <p className="text-2xl font-bold">{redZones}</p>
        </div>
      </div>

      <div className="mb-4">
        <p className="font-medium">Dificultad:</p>
        <p className="text-lg">
          {difficulty} (profundidad {difficultyDepth[difficulty]})
        </p>
      </div>

      <div
        className={`p-2 rounded-md text-center font-bold ${
          isGreenTurn ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
        }`}
      >
        {statusMessage}
      </div>
    </div>
  )
}
