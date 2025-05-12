"use client"

import type { Difficulty } from "./yoshis-zones-game"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface DifficultySelectorProps {
  difficulty: Difficulty
  setDifficulty: (difficulty: Difficulty) => void
  onNewGame: () => void
}

export default function DifficultySelector({ difficulty, setDifficulty, onNewGame }: DifficultySelectorProps) {
  const handleDifficultyChange = (value: string) => {
    setDifficulty(value as Difficulty)
  }

  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 w-full max-w-md">
      <div className="w-full sm:w-2/3">
        <Select value={difficulty} onValueChange={handleDifficultyChange}>
          <SelectTrigger>
            <SelectValue placeholder="Selecciona dificultad" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="beginner">Principiante (profundidad 2)</SelectItem>
            <SelectItem value="amateur">Amateur (profundidad 4)</SelectItem>
            <SelectItem value="expert">Experto (profundidad 6)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button onClick={onNewGame} className="w-full sm:w-1/3 bg-green-600 hover:bg-green-700">
        Nuevo juego
      </Button>
    </div>
  )
}
