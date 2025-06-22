import React from "react";

export interface GenericEvent {
  url: string; // Obrigatória
  name?: string;
  date?: string;
  place_name?: string;
  address?: string;
  subinfos?: string[];
  description_cropped?: string;
  classification?: string;
  parcelamento?: string;
  nome_organizador?: string;
}

interface CardProps {
  event?: GenericEvent; // Opcional
}

const Card: React.FC<CardProps> = ({ event }) => {
  // Se event for undefined, usamos um objeto com url vazia e outros valores padrão
  const safeEvent = event || { url: "#" };

  const {
    url,
    name = "(Nome não fornecido)",
    date = "(Data não fornecida)",
    place_name = "(Local não especificado)",
    address = "(Endereço não disponível)",
    subinfos = [],
    description_cropped,
    classification = "(Classificação não informada)",
    parcelamento = "(Formas de pagamento não especificadas)",
    nome_organizador = "(Organizador não informado)",
  } = safeEvent;

  return (
    <div className="card">
      <h2>{name}</h2>
      <p className="date">{date}</p>
      <div className="local-info">
        <h3>{place_name}</h3>
        <p>{address}</p>
      </div>
      <p className="description">
        {description_cropped
          ? description_cropped.endsWith("...")
            ? description_cropped
            : `${description_cropped}...`
          : "(Descrição não fornecida)"}
      </p>
      <p className="classification">{classification}</p>
      <p className="parcelamento">{parcelamento}</p>
      <p className="organizador">Organizador: {nome_organizador}</p>
      <div className="subinfos">
        {subinfos.length > 0 ? (
          subinfos.map((info, i) => <p key={i}>{info}</p>)
        ) : (
          <p>(Informações adicionais não disponíveis)</p>
        )}
      </div>
      <a href={url} target="_blank" rel="noopener noreferrer" className="btn">
        Ver evento completo
      </a>
    </div>
  );
};

export default Card;
