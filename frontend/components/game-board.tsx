"use client"

import type { CellState, Position } from "./yoshis-zones-game"
import GameCell from "./game-cell"

interface GameBoardProps {
  board: CellState[][]
  specialZones: Position[][]
  validMoves: Position[]
  onCellClick: (row: number, col: number) => void
}

export default function GameBoard({ board, specialZones, validMoves, onCellClick }: GameBoardProps) {
  // Verificar si una posición está en una zona especial
  const isSpecialZone = (row: number, col: number): boolean => {
    return specialZones.some((zone) => zone.some((pos) => pos.row === row && pos.col === col))
  }

  // Verificar si una posición es un movimiento válido
  const isValidMove = (row: number, col: number): boolean => {
    return validMoves.some((move) => move.row === row && move.col === col)
  }

  return (
    <div className="grid grid-cols-8 gap-0.5 border-2 border-gray-800 bg-gray-800 w-full max-w-md">
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => (
          <GameCell
            key={`${rowIndex}-${colIndex}`}
            state={cell}
            isSpecialZone={isSpecialZone(rowIndex, colIndex)}
            isValidMove={isValidMove(rowIndex, colIndex)}
            isDarkSquare={(rowIndex + colIndex) % 2 === 1}
            onClick={() => onCellClick(rowIndex, colIndex)}
          />
        )),
      )}
    </div>
  )
}
