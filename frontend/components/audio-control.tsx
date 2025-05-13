"use client"

import { Button } from "@/components/ui/button"
import { Volume2, VolumeX } from 'lucide-react'

interface AudioControlProps {
  isMuted: boolean
  toggleMute: () => void
}

export default function AudioControl({ isMuted, toggleMute }: AudioControlProps) {
  return (
    <Button
      onClick={toggleMute}
      variant="outline"
      size="icon"
      className="bg-white/90 backdrop-blur-sm hover:bg-white/70"
      aria-label={isMuted ? "Activar sonido" : "Silenciar sonido"}
    >
      {isMuted ? <VolumeX className="h-5 w-5 text-red-500" /> : <Volume2 className="h-5 w-5 text-green-600" />}
    </Button>
  )
}