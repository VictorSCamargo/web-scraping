import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Card, { type GenericEvent } from './components/Card';
import { type BlueticketEvent, convertBlueticketEventToGeneric } from './utils/convertBlueticketEventToGeneric';

function App() {
  const [allEvents, setAllEvents] = useState<GenericEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Carrega todos os eventos de uma vez
  useEffect(() => {
    const loadAllEvents = async () => {
      try {
        const blueticketResponse = await fetch('/blueticket.json');
        const blueticketData: BlueticketEvent[] = await blueticketResponse.json();
        const blueticketConvertedEvents = blueticketData.map(convertBlueticketEventToGeneric);

        // ToDo ajustar para os outros sites
        const website2Response = await fetch('/blueticket.json');
        const website2Data: BlueticketEvent[] = await website2Response.json();
        const website2ConvertedEvents = website2Data.map(convertBlueticketEventToGeneric);

        // const website3Response = await fetch('/blueticket.json');
        // const website3Data: BlueticketEvent[] = await website3Response.json();
        // const website3ConvertedEvents = website3Data.map(convertBlueticketEventToGeneric);

        // ToDo ajustar para outros sites
        const events = [...blueticketConvertedEvents, ...website2ConvertedEvents]


        setAllEvents(events);
        // Mostra o primeiro lote de eventos
        // setVisibleEvents(convertedEvents.slice(0, batchSize));
      } catch (error) {
        console.error('Erro ao carregar eventos:', error);
      } finally {
        setLoading(false);
      }
    };

    loadAllEvents();
  }, []);

  return (
    <div className="app">
      <h1>Eventos</h1>
      {!loading && <h2>Total de eventos: {allEvents.length}</h2>}
      <div className="cards-container">
        {allEvents.map((event, index) => (
          <Card key={`${event.url}-${index}`} event={event} />
        ))}
      </div>
      {loading && <div className="loading">Carregando...</div>}
    </div>
  );
}

export default App;