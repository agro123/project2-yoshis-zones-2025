// src/components/GameOverScreen.tsx
import React from "react";

interface GameOverScreenProps {
  winner: "green" | "red" | "draw";
  onRestart: () => void;
}

const GameOverScreen: React.FC<GameOverScreenProps> = ({ winner, onRestart }) => {
  let message = "";
  let imagePath = "";
  let imageClass ="";

  switch (winner) {
    case "green":
      message = "¡Gana Yoshi verde!";
      imagePath = "/images/green-yoshi.png";
      imageClass = "w-64";
      break;
    case "red":
      message = "¡Gana Yoshi rojo!";
      imagePath = "/images/red-yoshi.png";
      imageClass = "w-64";
      break;
    case "draw":
      message = "¡Empate!";
      imagePath = "/images/empate.png";
      imageClass = "w-45";
      break;
   
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center text-white z-50">
      <img src={imagePath} alt="Resultado" className={`${imageClass} mb-6`} />
      <h2 className="text-3xl font-bold mb-4">{message}</h2>
      <button
        onClick={onRestart}
        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-xl shadow-xl"
      >
        Volver a jugar
      </button>
    </div>
  );
};

export default GameOverScreen;
