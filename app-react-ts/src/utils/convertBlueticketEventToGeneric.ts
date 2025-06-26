import type { BlueticketEvent, GenericEvent } from "../model/eventos-model";

export function convertBlueticketEventToGeneric(
  event: BlueticketEvent
): GenericEvent {
  return {
    url: event.url,
    name: event.name,
    date: event.date,
    place_name: event["local-subtitle"],
    address: event["local-description"],
    subinfos: event.subinfos,
    description_cropped: event.description_cropped,
    classification: event.classification,
    parcelamento: event.parcelamento,
    nome_organizador: event.nome_organizador,
  };
}
