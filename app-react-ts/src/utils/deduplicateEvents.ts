import stringSimilarity from "string-similarity";
import type { GenericEvent } from "../components/Card";

// Com base em um percentual de similaridade remove eventos duplicados
export function deduplicateEvents(events: GenericEvent[]): GenericEvent[] {
  const result: GenericEvent[] = [];

  for (const current of events) {
    const isDuplicate = result.some((existing) => {
      if (current.name && existing.name) {
        const similarity = stringSimilarity.compareTwoStrings(
          current.name,
          existing.name,
        );
        return similarity >= 0.95;
      }
    });

    if (!isDuplicate) {
      result.push(current);
    }
  }

  return result;
}
