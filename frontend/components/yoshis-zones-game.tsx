"use client"

import { useState, useEffect } from "react"
import GameBoard from "./game-board"
import GameInfo from "./game-info"
import DifficultySelector from "./difficulty-selector"
import AudioControl from "./audio-control"

// Tipos para el juego
export type CellState = "empty" | "green-yoshi" | "red-yoshi" | "green-painted" | "red-painted"
export type Position = { row: number; col: number }
export type Difficulty = "beginner" | "amateur" | "expert"
export type GameStatus = "playing" | "green-wins" | "red-wins" | "draw"

export default function YoshisZonesGame() {
  // Estado del tablero (8x8)
  const [board, setBoard] = useState<CellState[][]>(
    Array(8)
      .fill(null)
      .map(() => Array(8).fill("empty")),
  )

  // Posiciones de los Yoshis
  const [greenYoshiPosition, setGreenYoshiPosition] = useState<Position | null>(null)
  const [redYoshiPosition, setRedYoshiPosition] = useState<Position | null>(null)

  // Contadores de zonas
  const [greenZones, setGreenZones] = useState(0)
  const [redZones, setRedZones] = useState(0)

  // Turno actual (true = verde, false = rojo)
  const [isGreenTurn, setIsGreenTurn] = useState(true)

  // Estado del juego
  const [gameStatus, setGameStatus] = useState<GameStatus>("playing")

  // Dificultad seleccionada
  const [difficulty, setDifficulty] = useState<Difficulty>("beginner")

  // Estado del audio
  const [isMuted, setIsMuted] = useState(false)

  // Zonas especiales (esquinas)
  const specialZones: Position[][] = [
    // Esquina superior izquierda
    [
      { row: 0, col: 0 },
      { row: 0, col: 1 },
      { row: 1, col: 0 },
      { row: 1, col: 1 },
      { row: 0, col: 2 },
    ],
    // Esquina superior derecha
    [
      { row: 0, col: 7 },
      { row: 0, col: 6 },
      { row: 1, col: 7 },
      { row: 1, col: 6 },
      { row: 0, col: 5 },
    ],
    // Esquina inferior izquierda
    [
      { row: 7, col: 0 },
      { row: 7, col: 1 },
      { row: 6, col: 0 },
      { row: 6, col: 1 },
      { row: 7, col: 2 },
    ],
    // Esquina inferior derecha
    [
      { row: 7, col: 7 },
      { row: 7, col: 6 },
      { row: 6, col: 7 },
      { row: 6, col: 6 },
      { row: 7, col: 5 },
    ],
  ]

  // Verificar si una posición está en una zona especial
  const isInSpecialZone = (position: Position): boolean => {
    return specialZones.some((zone) => zone.some((pos) => pos.row === position.row && pos.col === position.col))
  }

  // Generar posición aleatoria fuera de zonas especiales
  const generateRandomPosition = (): Position => {
    let position: Position
    do {
      position = {
        row: Math.floor(Math.random() * 8),
        col: Math.floor(Math.random() * 8),
      }
    } while (isInSpecialZone(position))
    return position
  }

// Manejar el cambio de estado del audio
const toggleMute = () => {
  setIsMuted(!isMuted)
  // Aquí podrías añadir lógica adicional para silenciar/activar el audio de fondo
}


  // Inicializar el juego
  const initializeGame = () => {
    // Crear un nuevo tablero vacío
    const newBoard: CellState[][] = Array(8)
      .fill(null)
      .map(() => Array(8).fill("empty"))

    // Generar posiciones aleatorias para los Yoshis
    const greenPos = generateRandomPosition()
    let redPos

    // Asegurarse de que los Yoshis no estén en la misma posición
    do {
      redPos = generateRandomPosition()
    } while (redPos.row === greenPos.row && redPos.col === greenPos.col)

    // Colocar los Yoshis en el tablero
    newBoard[greenPos.row][greenPos.col] = "green-yoshi"
    newBoard[redPos.row][redPos.col] = "red-yoshi"

    // Actualizar el estado
    setBoard(newBoard)
    setGreenYoshiPosition(greenPos)
    setRedYoshiPosition(redPos)
    setIsGreenTurn(true)
    setGreenZones(0)
    setRedZones(0)
    setGameStatus("playing")
    // Reproducir sonido de inicio de juego (cuando se implemente el audio)
    playSound("gameStart")
  }

// Función para reproducir sonidos (placeholder para futura implementación)
const playSound = (soundType: string) => {
  if (isMuted) return // No reproducir si está silenciado

  // PUNTO DE INTEGRACIÓN CON AUDIO #1:
  // Aquí se implementaría la lógica para reproducir diferentes sonidos
  // según el tipo de sonido solicitado
  /*
  const sounds = {
    gameStart: '/sounds/game-start.mp3',
    move: '/sounds/move.mp3',
    capture: '/sounds/capture.mp3',
    win: '/sounds/win.mp3',
    lose: '/sounds/lose.mp3'
  };
  
  const audio = new Audio(sounds[soundType]);
  audio.play().catch(e => console.error('Error al reproducir audio:', e));
  */

  console.log(`Sonido reproducido: ${soundType} (silenciado: ${isMuted})`)
}


  // Calcular movimientos válidos para un Yoshi (movimiento de caballo)
  const getValidMoves = (position: Position): Position[] => {
    if (!position) return []

    const { row, col } = position
    const possibleMoves = [
      { row: row - 2, col: col - 1 },
      { row: row - 2, col: col + 1 },
      { row: row - 1, col: col - 2 },
      { row: row - 1, col: col + 2 },
      { row: row + 1, col: col - 2 },
      { row: row + 1, col: col + 2 },
      { row: row + 2, col: col - 1 },
      { row: row + 2, col: col + 1 },
    ]

    // Filtrar movimientos dentro del tablero y que no estén ocupados por otro Yoshi
    return possibleMoves.filter((move) => {
      const isInBoard = move.row >= 0 && move.row < 8 && move.col >= 0 && move.col < 8
      if (!isInBoard) return false

      const cell = board[move.row][move.col]
      return cell !== "green-yoshi" && cell !== "red-yoshi"
    })
  }

  // Actualizar la función handlePlayerMove para que maneje el movimiento del jugador (Yoshi rojo)
  const handlePlayerMove = (row: number, col: number) => {
    if (isGreenTurn || gameStatus !== "playing" || !redYoshiPosition) return

    // Verificar si el movimiento es válido
    const validMoves = getValidMoves(redYoshiPosition)
    const isValidMove = validMoves.some((move) => move.row === row && move.col === col)

    if (!isValidMove) return

    // Crear una copia del tablero
    const newBoard = [...board.map((row) => [...row])]

    // Actualizar la posición anterior del Yoshi rojo
    newBoard[redYoshiPosition.row][redYoshiPosition.col] = "red-painted"

    // Mover el Yoshi rojo a la nueva posición
    newBoard[row][col] = "red-yoshi"

    // Actualizar el estado
    setBoard(newBoard)
    setRedYoshiPosition({ row, col })
    setIsGreenTurn(true)
    // Reproducir sonido de movimiento
    playSound("move")
   // Aquí se conectaría con la lógica de IA para el movimiento del Yoshi verde
   // Por ahora, simplemente cambiamos el turno de vuelta al jugador después de un tiempo
   setTimeout(() => {
     // Simular un movimiento aleatorio del Yoshi verde
     simulateGreenYoshiMove()
   }, 500)

    // Verificar si se ha ganado alguna zona
    checkZones()
  }

  // Añadir una función para simular el movimiento del Yoshi verde (máquina)
  const simulateGreenYoshiMove = () => {
    if (!greenYoshiPosition || gameStatus !== "playing") return

    const validMoves = getValidMoves(greenYoshiPosition)
    if (validMoves.length === 0) return

    // Seleccionar un movimiento aleatorio
    const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)]

    // Crear una copia del tablero
    const newBoard = [...board.map((row) => [...row])]

    // Actualizar la posición anterior del Yoshi verde
    newBoard[greenYoshiPosition.row][greenYoshiPosition.col] = "green-painted"

    // Mover el Yoshi verde a la nueva posición
    newBoard[randomMove.row][randomMove.col] = "green-yoshi"

    // Actualizar el estado
    setBoard(newBoard)
    setGreenYoshiPosition(randomMove)
    setIsGreenTurn(false)
    // Reproducir sonido de movimiento
    playSound("move")

    // Verificar si se ha ganado alguna zona
    checkZones()
  }

  // Verificar si alguna zona especial ha sido capturada
  const checkZones = () => {
    // Esta función verificaría si alguna zona especial ha sido completamente
    // pintada de un color y actualizaría los contadores
    // Por ahora es un placeholder para la futura implementación
  }

  // Inicializar el juego al cargar el componente
  useEffect(() => {
    initializeGame()
  }, [])

  return (
    <div className="flex flex-col items-center gap-6 w-full max-w-4xl">
  <div className="flex flex-col sm:flex-row items-center justify-between w-full max-w-2xl gap-4">
    <DifficultySelector difficulty={difficulty} setDifficulty={setDifficulty} onNewGame={initializeGame} />
    <AudioControl isMuted={isMuted} toggleMute={toggleMute} />
  </div>

      <div className="flex flex-col md:flex-row gap-6 w-full items-center">
        <GameBoard
          board={board}
          specialZones={specialZones}
          validMoves={!isGreenTurn && redYoshiPosition ? getValidMoves(redYoshiPosition) : []}
          onCellClick={handlePlayerMove}
        />

        <GameInfo
          greenZones={greenZones}
          redZones={redZones}
          isGreenTurn={isGreenTurn}
          gameStatus={gameStatus}
          difficulty={difficulty}
        />
      </div>
    </div>
  )
}
