"use client"

import type { CellState } from "./yoshis-zones-game"

interface GameCellProps {
  state: CellState
  isSpecialZone: boolean
  isValidMove: boolean
  isDarkSquare: boolean
  onClick: () => void
}

export default function GameCell({ state, isSpecialZone, isValidMove, isDarkSquare, onClick }: GameCellProps) {
  // Determinar el color base de la celda (tablero de ajedrez)
  const baseColor = isDarkSquare ? "bg-gray-300" : "bg-white"

  // Determinar el color si está pintada
  let cellColor = baseColor
  if (state === "green-painted") {
    cellColor = "bg-green-200"
  } else if (state === "red-painted") {
    cellColor = "bg-red-200"
  }

  // Añadir borde si es una zona especial
  const specialZoneClass = isSpecialZone ? "border-2 border-yellow-400" : ""

  // Añadir indicador de movimiento válido
  const validMoveClass = isValidMove
    ? "after:content-[''] after:absolute after:inset-0 after:bg-blue-400 after:opacity-30 after:rounded-full after:m-auto after:w-2/3 after:h-2/3"
    : ""

  return (
    <div
      className={`relative w-full aspect-square ${cellColor} ${specialZoneClass} ${validMoveClass} flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity`}
      onClick={onClick}
    >
      {state === "green-yoshi" && (
        <div className="absolute inset-0 flex items-center justify-center">
          <img src="/images/green-yoshi.png" alt="Green Yoshi" className="w-4/5 h-4/5 object-contain" />
        </div>
      )}

      {state === "red-yoshi" && (
        <div className="absolute inset-0 flex items-center justify-center">
          <img src="/images/red-yoshi.png" alt="Red Yoshi" className="w-4/5 h-4/5 object-contain" />
        </div>
      )}
    </div>
  )
}
