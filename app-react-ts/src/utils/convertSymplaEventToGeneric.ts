import type { GenericEvent, SymplaEvent } from "../model/eventos-model";

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
