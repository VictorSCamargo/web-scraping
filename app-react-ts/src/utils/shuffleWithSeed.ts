import seedrandom from 'seedrandom';

// Função para embaralhar array com seed fixa
export function shuffleWithSeed<T>(array: T[], seed: string): T[] {
  const rng = seedrandom(seed); // PRNG com seed
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1)); // Usa o RNG com seed
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]; // Troca os elementos
  }
  return shuffled;
}