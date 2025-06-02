import type { GenericEvent } from "../components/Card";

export interface BlueticketEvent {
  url: string;
  name?: string;
  date?: string;
  'local-subtitle'?: string;
  'local-description'?: string;
  subinfos?: string[];
  description_cropped?: string;
  classification?: string;
  parcelamento?: string;
  nome_organizador?: string;
}

export function convertBlueticketEventToGeneric(event: BlueticketEvent): GenericEvent {
  return {
    url: event.url,
    name: event.name,
    date: event.date,
    place_name: event['local-subtitle'],
    address: event['local-description'],
    subinfos: event.subinfos,
    description_cropped: event.description_cropped,
    classification: event.classification,
    parcelamento: event.parcelamento,
    nome_organizador: event.nome_organizador
  };
}