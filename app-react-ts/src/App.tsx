import { useState, useEffect, Fragment } from "react";
import "./css/App.css";

import { convertBlueticketEventToGeneric } from "./utils/convertBlueticketEventToGeneric";
import { shuffleWithSeed } from "./utils/shuffleWithSeed";
import { deduplicateEvents } from "./utils/deduplicateEvents";
import CardContainer from "./components/CardContainer";
import Pagination from "./components/Pagination";
import { convertSymplaEventToGeneric } from "./utils/convertSymplaEventToGeneric";
import { SearchBar } from "./components/SearchBar";
import type {
  BlueticketEvent,
  GenericEvent,
  SymplaEvent,
} from "./model/eventos-model";

export default function App() {
  const [allEvents, setAllEvents] = useState<GenericEvent[]>([]);
  const [filteredEvents, setFilteredEvents] = useState<GenericEvent[]>([]);
  const [searchInput, setSearchInput] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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

        const shuffledEvents = shuffleWithSeed(events, "seedfixa");
        const deduplicatedEvents = deduplicateEvents(shuffledEvents);

        setAllEvents(deduplicatedEvents);
      } catch (error) {
        setError((error as Error).message || "Erro desconhecido");
      } finally {
        setLoading(false);
      }
    };

    loadAllEvents();
  }, []);

  const handleSearch = () => {
    const lower = searchInput.toLowerCase().trim();
    const result = allEvents.filter(
      (event) => event?.name?.toLowerCase().includes(lower) ?? false
    );
    setFilteredEvents(result);
    setCurrentPage(1);
  };

  const eventsPerPage = 6;
  const hasFilteredEvents = filteredEvents.length > 0;
  const eventsToDisplay = hasFilteredEvents ? filteredEvents : allEvents;

  const indexOfLastEvent = currentPage * eventsPerPage;
  const indexOfFirstEvent = indexOfLastEvent - eventsPerPage;

  const currentEvents = eventsToDisplay.slice(
    indexOfFirstEvent,
    indexOfLastEvent
  );

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  return (
    <div className="app">
      <h1 className="title-main">Eventos</h1>

      {error && <div style={{ color: "red" }}>Erro: {error}</div>}

      {loading ? (
        <div className="loading">Carregando...</div>
      ) : (
        <Fragment>
          <SearchBar
            searchInput={searchInput}
            setSearchInput={setSearchInput}
            handleSearch={handleSearch}
          />
          <h2 className="title-sub">
            Total de eventos: {eventsToDisplay.length}
          </h2>
          <CardContainer events={currentEvents} />
          <Pagination
            eventsPerPage={eventsPerPage}
            totalEvents={eventsToDisplay.length}
            paginate={paginate}
          />
        </Fragment>
      )}
    </div>
  );
}
