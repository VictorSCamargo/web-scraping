import React from 'react';

const Card = ({ event }) => {
  return (
    <div className="card">
      <h2>{event.name}</h2>
      <p className="date">{event.date}</p>
      <div className="local-info">
        <h3>{event['local-subtitle']}</h3>
        <p>{event['local-description']}</p>
      </div>
      <p className="description">{event.description_cropped}</p>
      <div className="subinfos">
        {event.subinfos.map((info, i) => (
          <p key={i}>{info}</p>
        ))}
      </div>
      <p className="classification">{event.classification}</p>
      <p className="parcelamento">{event.parcelamento}</p>
      <p className="organizador">Organizador: {event.nome_organizador}</p>
      <a href={event.url} target="_blank" rel="noopener noreferrer" className="btn">
        Ver detalhes
      </a>
    </div>
  );
};

export default Card;