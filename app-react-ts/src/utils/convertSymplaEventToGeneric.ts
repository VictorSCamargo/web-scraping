import type { GenericEvent } from "../components/Card";

export interface SymplaEvent {
  link: string;
  titulo?: string;
  data?: string;
  "local-subtitle"?: string;
  "local-description"?: string;
  politicas_evento?: string[];
  descricao?: string;
  classification?: string;
  parcelamento?: string;
  nome_organizador?: string;
}

export function convertSymplaEventToGeneric(event: SymplaEvent): GenericEvent {
  return {
    url: event.link,
    name: event.titulo,
    date: event.data,
    place_name: event["local-subtitle"],
    address: event["local-description"],
    subinfos: event.politicas_evento,
    description_cropped: event.descricao?.slice(0, 100),
    classification: event.classification,
    parcelamento: event.parcelamento,
    nome_organizador: event.nome_organizador,
  };
}
