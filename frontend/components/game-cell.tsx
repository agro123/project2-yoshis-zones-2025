"use client"

import type { CellState } from "./yoshis-zones-game"

interface BorderConfig {
  top?: boolean
  bottom?: boolean
  left?: boolean
  right?: boolean
}

interface GameCellProps {
  state: CellState
  isSpecialZone: boolean
  isValidMove: boolean
  isDarkSquare: boolean
  onClick: () => void
  borderConfig?: BorderConfig // Agregar esta propiedad
}

export default function GameCell({ state, isSpecialZone, isValidMove, isDarkSquare, onClick, borderConfig }: GameCellProps) {
  // Determinar el color base de la celda (tablero de ajedrez)
  const baseColor = isDarkSquare ? "bg-gray-300" : "bg-white"

  // Determinar el color si está pintada
  let cellColor = baseColor
  if (state === "green-painted") {
    cellColor = "bg-green-400"
  } else if (state === "red-painted") {
    cellColor = "bg-red-400"
  }
  
  // Aplicar bordes personalizados tipo "paredes"
  const borderClasses = borderConfig
    ? [
        borderConfig.top ? "border-t-4 border-black" : "",
        borderConfig.bottom ? "border-b-4 border-black" : "",
        borderConfig.left ? "border-l-4 border-black" : "",
        borderConfig.right ? "border-r-4 border-black" : ""
      ].join(" ")
    : ""

  // Añadir borde si es una zona especial
  const specialZoneClass = isSpecialZone
  ? "border-2 border-black shadow-[0_0_8px_8px_rgba(233,179,8,0.5)]"
  : "";

  // Añadir indicador de movimiento válido
  const validMoveClass = isValidMove
    ? "after:content-[''] after:absolute after:inset-0 after:bg-blue-400 after:opacity-30 after:rounded-full after:m-auto after:w-2/3 after:h-2/3"
    : ""
    
  return (
    <div
      className={`relative w-full aspect-square ${cellColor} ${specialZoneClass} ${validMoveClass} ${borderClasses} flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity`}
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
