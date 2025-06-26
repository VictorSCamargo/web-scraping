export type GenericEvent = {
  url: string;
  name?: string;
  date?: string;
  place_name?: string;
  address?: string;
  subinfos?: string[];
  description_cropped?: string;
  classification?: string;
  parcelamento?: string;
  nome_organizador?: string;
};

export type BlueticketEvent = {
  url: string;
  name?: string;
  date?: string;
  "local-subtitle"?: string;
  "local-description"?: string;
  subinfos?: string[];
  description_cropped?: string;
  classification?: string;
  parcelamento?: string;
  nome_organizador?: string;
};

export type SymplaEvent = {
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
};
