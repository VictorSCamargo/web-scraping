import { useState, useEffect } from "react";
import "./App.css";
import { type GenericEvent } from "./components/Card";
import {
  type BlueticketEvent,
  convertBlueticketEventToGeneric,
} from "./utils/convertBlueticketEventToGeneric";
import { shuffleWithSeed } from "./utils/shuffleWithSeed";
import { deduplicateEvents } from "./utils/deduplicateEvents";
import CardContainer from "./components/CardContainer";
import Pagination from "./components/Pagination";
import {
  convertSymplaEventToGeneric,
  type SymplaEvent,
} from "./utils/convertSymplaEventToGeneric";

function App() {
  const [allEvents, setAllEvents] = useState<GenericEvent[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [eventsPerPage, setEventsPerPage] = useState(6);
  const [loading, setLoading] = useState<boolean>(true);

  // Carrega todos os eventos de uma vez
  useEffect(() => {
    const loadAllEvents = async () => {
      try {
        const blueticketResponse = await fetch("/blueticket.json");
        const blueticketData: BlueticketEvent[] =
          await blueticketResponse.json();
        const blueticketConvertedEvents = blueticketData.map(
          convertBlueticketEventToGeneric
        );

        const symplaResponse = await fetch("/eventos_sympla_backup.json");
        const symplaData: SymplaEvent[] = await symplaResponse.json();
        const symplaConvertedEvents = symplaData.map(
          convertSymplaEventToGeneric
        );

        const pensaNoEventoResponse = await fetch("/pensanoevento.json");
        const pensaNoEventoData: GenericEvent[] =
          await pensaNoEventoResponse.json();

        const events = [
          ...pensaNoEventoData,
          ...blueticketConvertedEvents,
          ...symplaConvertedEvents,
        ];

        // Shuffle com uma seed fixa para dar um ar de aleatoriedade inicialmente caso não seja usado outro filtro
        const shuffledEvents = shuffleWithSeed(events, "seedfixa");
        const deduplicatedEvents = deduplicateEvents(shuffledEvents);

        setAllEvents(deduplicatedEvents);
        // Mostra o primeiro lote de eventos
        // setVisibleEvents(convertedEvents.slice(0, batchSize));
      } catch (error) {
        console.error("Erro ao carregar eventos:", error);
      } finally {
        setLoading(false);
      }
    };

    loadAllEvents();
  }, []);

  const indexOfLastEvent = currentPage * eventsPerPage;
  const indexOfFirstEvent = indexOfLastEvent - eventsPerPage;
  const currentEvents = allEvents.slice(indexOfFirstEvent, indexOfLastEvent);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <div className="app">
      <h1>Eventos</h1>
      {!loading && <h2>Total de eventos: {allEvents.length}</h2>}
      <CardContainer events={currentEvents} />
      {!loading && (
        <Pagination
          eventsPerPage={eventsPerPage}
          totalEvents={allEvents.length}
          paginate={paginate}
        />
      )}
      {loading && <div className="loading">Carregando...</div>}
    </div>
  );
}

export default App;
