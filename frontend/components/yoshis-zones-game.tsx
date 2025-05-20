"use client"

import { useState, useEffect ,useRef, useMemo, useCallback } from "react"
import GameBoard from "./game-board"
import GameInfo from "./game-info"
import DifficultySelector from "./difficulty-selector"
import AudioControl from "./audio-control"
import GameOverScreen from "./GameOverScreen";


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
  const [isMuted, setIsMuted] = useState(true)
  
  const [audiogame, setAudioGame] = useState("gameStart")
  //Casillas marcadas
  const [redCells, setRedCells] = useState<any[]>([])
  const [greenCells, setGreenCells] = useState<any[]>([])


  // Referencias para los audios
  const backgroundMusicRef = useRef<HTMLAudioElement | null>(null)
  
  // Estado para notificaciones
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [notificationCounter, setNotificationCounter] = useState(0)

  const [winner, setWinner] = useState<"green" | "red" | "draw" | null>(null);


  
  useEffect(() => {
  if (!backgroundMusicRef.current) {
    backgroundMusicRef.current = new Audio("/sounds/play.mp3");
    backgroundMusicRef.current.loop = true;
    backgroundMusicRef.current.volume = 0.5;
  }

  if (!isMuted) {
    backgroundMusicRef.current.play().catch(e =>
      console.warn("No se pudo reproducir el audio automáticamente:", e)
    );
  } else {
    backgroundMusicRef.current.pause();
  }
}, [isMuted]);


  useEffect(() => {
  if (gameStatus !== "playing" && backgroundMusicRef.current) {
    backgroundMusicRef.current.pause();
    backgroundMusicRef.current.currentTime = 0;
  }
  
}, [gameStatus]);





  // Zonas especiales (esquinas)
  const specialZones: Position[][] = [
    // Esquina superior izquierda
    [
      { row: 0, col: 0 },
      { row: 0, col: 1 },
      { row: 1, col: 0 },
      { row: 2, col: 0 },
      { row: 0, col: 2 },
    ],
    // Esquina superior derecha
    [
      { row: 0, col: 7 },
      { row: 0, col: 6 },
      { row: 1, col: 7 },
      { row: 2, col: 7 },
      { row: 0, col: 5 },
    ],
    // Esquina inferior izquierda
    [
      { row: 7, col: 0 },
      { row: 7, col: 1 },
      { row: 6, col: 0 },
      { row: 5, col: 0 },
      { row: 7, col: 2 },
    ],
    // Esquina inferior derecha
    [
      { row: 7, col: 7 },
      { row: 7, col: 6 },
      { row: 6, col: 7 },
      { row: 5, col: 7 },
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
    setIsMuted(prev => !prev)
    // Aquí podrías añadir lógica adicional para silenciar/activar el audio de fondo
  }


  // Inicializar el juego
  const initializeGame = () => {
  setWinner(null); // oculta la pantalla de game over cuando reinicias

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
    setRedCells([])
    setGreenCells([])

    setGameStatus("playing")

    setTimeout(() => {
      // Simular un movimiento aleatorio del Yoshi verde
      //simulateGreenYoshiMove(greenPos, newBoard)
      getGreenYoshiMovement(greenPos, redPos, [], [], 0, 0, newBoard)
    }, 1000)
    // Reproducir sonido de inicio de juego (cuando se implemente el audio)
    playSound("gameStart")
  }

  // Función para reproducir sonidos (placeholder para futura implementación)
  // Función para reproducir sonidos
 const playSound = (soundType: string) => {
  if (isMuted) return; // No reproducir si está silenciado

  let soundPath = "";
  let soundMessage = "";

  switch (soundType) {
    case "gameStart":
      soundPath = "/sounds/play.mp3";
      soundMessage = "¡Nuevo juego iniciado!";
      break;
    case "move":
      soundPath = "/sounds/move.mp3";
      soundMessage = isGreenTurn ? "Yoshi verde ha movido" : "Has movido a Yoshi rojo";
      break;
    case "capture":
      soundMessage = isGreenTurn ? "¡Yoshi verde ha capturado una zona!" : "¡Has capturado una zona!";
      break;
    case "win":
      soundPath = "/sounds/winner.mp3";
      soundMessage = "¡Has ganado la partida!";
      break;
    case "lose":
      soundPath = "/sounds/game_over.mp3";
      soundMessage = "Has perdido la partida";
      break;
    case "draw":
      soundPath = "/sounds/emp.mp3";
      soundMessage = "La partida ha terminado en empate";
      break;
  }

if (soundPath) {
  const audio = new Audio(soundPath)
  audio.volume = 0.5
  audio.play().catch(e =>
    console.warn("No se pudo reproducir el audio automáticamente:", e)
  )
}


  // Aquí podrías mostrar el mensaje con un toast o algo similar
  // console.log(soundMessage)
};



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

    // Mover el Yoshi rojo a la nueva posición
    newBoard[row][col] = "red-yoshi"

    let newRedCells = [...redCells]
    if(isInSpecialZone({row,col})){
      newRedCells = [...redCells, [row,col]]
      setRedCells(newRedCells)
    }

    // Actualizar la posición anterior del Yoshi rojo
    if(isInSpecialZone(redYoshiPosition)){
      newBoard[redYoshiPosition.row][redYoshiPosition.col] = "red-painted"
    } else {
      newBoard[redYoshiPosition.row][redYoshiPosition.col] = "empty"
    }

    const newPos = { row, col }
    // Actualizar el estado
    setBoard(newBoard)
    setRedYoshiPosition(newPos)
    setIsGreenTurn(true)
    // Reproducir sonido de movimiento
    playSound("move")

    // Verificar si se ha ganado alguna zona
    const [gz, rz] = checkZones(newRedCells, greenCells)

    // Aquí se conectaría con la lógica de IA para el movimiento del Yoshi verde
    // Por ahora, simplemente cambiamos el turno de vuelta al jugador después de un tiempo
    setTimeout(() => {
      if(greenYoshiPosition) {
        // Simular un movimiento aleatorio del Yoshi verde
        //simulateGreenYoshiMove(greenYoshiPosition, newBoard)
        //Obtener movimiento de Yoshi Verde
        getGreenYoshiMovement(greenYoshiPosition, newPos, greenCells, newRedCells, gz, rz,newBoard)
      }

    }, 500)


       if (isGameOver()) {
   getWinnerMessage(); // actualiza el estado `winner` para mostrar pantalla visual
   setGameStatus(
    greenZones > redZones
      ? "green-wins"
      : redZones > greenZones
      ? "red-wins"
      : "draw"
  );
  return;
}


  }

  // Añadir una función para simular el movimiento del Yoshi verde (máquina)
  const getGreenYoshiMovement = async (currGreenYoshiPos: Position, currRedYoshiPos: Position, currGreenCells: any, currRedCells: any, currGreenZones: number, currRedZones: number,  currBoard: CellState[][]) => {
    try {
      const _greenPos = currGreenYoshiPos
      if (!_greenPos || gameStatus !== "playing") return
      const validMoves = getValidMoves(_greenPos)

      if (validMoves.length === 0) return

      const response = await fetch('http://127.0.0.1:5000/play', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "pos_verde": [_greenPos.row, _greenPos.col],
          "pos_rojo": [currRedYoshiPos.row, currRedYoshiPos.col],
          "casillas_verde": currGreenCells,
          "casillas_rojo": currRedCells,
          "zonas_verde": currGreenZones,
          "zonas_rojo": currRedZones,
          "dificultad": difficulty
        })
      });

      if (!response.ok) {
        throw new Error('Error en la petición');
      }
  
      const [row, col]: [number, number] = await response.json();
      const newMove: Position = {row,col}
      console.log('Respuesta del servidor:', newMove);

      // Crear una copia del tablero
      const newBoard = [...currBoard.map((r) => [...r])]
      let newGreenCells = [...currGreenCells]
      if(isInSpecialZone(newMove)){
        newGreenCells = [...currGreenCells, [row,col]]
        setGreenCells(newGreenCells)
      }

      // Actualizar la posición anterior del Yoshi verde
      if(isInSpecialZone(_greenPos)){
        newBoard[_greenPos.row][_greenPos.col] = "green-painted"
      } else {
        newBoard[_greenPos.row][_greenPos.col] = "empty"
      }

      // Mover el Yoshi verde a la nueva posición
      newBoard[newMove.row][newMove.col] = "green-yoshi"
      // Actualizar el estado
      setBoard(newBoard)
      setGreenYoshiPosition(newMove)
      setIsGreenTurn(false)
      // Reproducir sonido de movimiento
      playSound("move")

      // Verificar si se ha ganado alguna zona
      checkZones(currRedCells, newGreenCells)
    } catch (error) {
      console.error('Error al hacer el POST:', error);
    }
  }

  // Verificar si alguna zona especial ha sido capturada
  const checkZones = (currenRedCells: any[], currentGreenCells: any[]) => {
    // Esta función verificaría si alguna zona especial ha sido completamente
    // pintada de un color y actualizaría los contadores
    let _greenZones = 0;
    let _redZones = 0;
    for (const specialZone of specialZones) {
      let _greenCells = 0
      let _redCells = 0
      for (const cell of specialZone) {
        _redCells += currenRedCells.filter(c => cell.row === c[0] && cell.col === c[1]).length
        _greenCells += currentGreenCells.filter(c => cell.row === c[0] && cell.col === c[1]).length
      }
      if(_greenCells >= 3)
        _greenZones++
      if(_redCells >= 3)
        _redZones++
    }
    setGreenZones(_greenZones)
    setRedZones(_redZones)
    if(_greenZones > 2){
      //gana verde
    }
      
    if(_redZones > 2){
      //gana rojo
    }
      
    if(_redZones === 2 && _greenZones === 2){
      //Empate
    }

    return [_greenZones, _redZones]
  }
  
function isGameOver(): boolean {
  return specialZones.flat().every(pos => {
    const cell = board[pos.row][pos.col];
    return cell === "green-painted" || cell === "red-painted";
  });
}

function getWinnerMessage(): void {
  if (greenZones > redZones) {
    setAudioGame("win");
    setWinner("green"); // nuevo: guardamos el ganador en estado
  } else if (redZones > greenZones) {
    setAudioGame("lose");
    setWinner("red");
  } else {
    setAudioGame("draw");
    setWinner("draw");
  }
}


useEffect(() => {
  if (gameStatus === "green-wins") {
    playSound("lose")
  } else if (gameStatus === "red-wins") {
    playSound("win")
  } else if (gameStatus === "draw") {
    playSound("draw")
  }
}, [gameStatus])


  // Inicializar el juego al cargar el componente
  // Se ejecuta solo una vez al montar el componente (inicializa juego y audio)
  useEffect(() => {
    initializeGame()

    if (!isMuted && backgroundMusicRef.current) {
      backgroundMusicRef.current.play().catch(e =>
        console.warn("No se pudo reproducir el audio automáticamente:", e)
      )
    }

    return () => {
      if (backgroundMusicRef.current) {
        backgroundMusicRef.current.pause()
        backgroundMusicRef.current = null
      }
    }
  }, []) // ✅ Solo al montar

  // Se ejecuta cada vez que cambia isMuted (para pausar o reproducir)
  useEffect(() => {
    if (backgroundMusicRef.current) {
      if (isMuted) {
        backgroundMusicRef.current.pause()
      } else {
        backgroundMusicRef.current.play().catch(e =>
          console.warn("No se pudo reanudar el audio:", e)
        )
      }
    }
  }, [isMuted]) // ✅ Solo controla el audio

  useEffect(() => {
  }, [gameStatus])
  
  const redMovements = useMemo(() => !isGreenTurn && redYoshiPosition ? getValidMoves(redYoshiPosition) : [] , [redYoshiPosition, isGreenTurn])

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
          validMoves={redMovements}
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
      {winner && <GameOverScreen winner={winner} onRestart={initializeGame} />}

    </div>
  )
}
