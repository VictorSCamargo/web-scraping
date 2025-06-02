import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Card, { type GenericEvent } from './components/Card';
import { type BlueticketEvent, convertBlueticketEventToGeneric } from './utils/convertBlueticketEventToGeneric';

type EventSource = 'blueticket' | 'fonte2' | 'fonte3';

function App() {
  const [allEvents, setAllEvents] = useState<GenericEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [initialLoad, setInitialLoad] = useState<boolean>(false);

  // Função para carregar eventos de uma fonte específica
  const loadEventsFromSource = useCallback(async (source: EventSource) => {
    if (loading || !hasMore) return;

    try {
      const response = await fetch(`/${source}.json`);
      // ToDo colocar os tipos dos outros eventos aqui também, que nem exemplo comentado abaixo
      const data: BlueticketEvent[] = await response.json();
      // let data: BlueticketEvent[] | Fonte2Event[] | Fonte3Event[] = await response.json();


      // Converte os eventos para GenericEvent
      const convertedEvents = data.map(event => {
        switch (source) {
          case 'blueticket': return convertBlueticketEventToGeneric(event);
          // ToDo outros
          // case 'fonte2': return convertFonte2ToGeneric(event);
          // case 'fonte3': return convertFonte3ToGeneric(event);
          default: throw new Error(`Fonte desconhecida: ${source}`);
        }
      });

      // Paginação (opcional)
      const itemsPerPage = 6;
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      const newEvents = convertedEvents.slice(startIndex, endIndex);

      if (newEvents.length === 0) {
        setHasMore(false);
      } else {
        setAllEvents(prevEvents => {
          const existingUrls = new Set(prevEvents.map(event => event.url));
          const uniqueNewEvents = newEvents.filter(event => !existingUrls.has(event.url));
          return [...prevEvents, ...uniqueNewEvents];
        });
        setPage(prevPage => prevPage + 1);
      }
    } catch (error) {
      console.error(`Erro ao carregar ${source}:`, error);
    } finally {
      setLoading(false);
    }
  }, [page, loading, hasMore]);

  // Carrega eventos de todas as fontes
  const loadAllEvents = useCallback(async () => {
    setLoading(true);
    await Promise.all([
      loadEventsFromSource('blueticket'),
      // ToDo
      loadEventsFromSource('blueticket'),
      // loadEventsFromSource('fonte3'),
    ]);
    setInitialLoad(true);
  }, [loadEventsFromSource]);

  // Carrega os primeiros eventos
  useEffect(() => {
    if (!initialLoad) loadAllEvents();
  }, [initialLoad, loadAllEvents]);

  // Rolagem infinita (igual ao seu código atual)
  useEffect(() => {
    if (!initialLoad) return;
    const handleScroll = () => {
      const scrollThreshold = 900;
      if (
        window.innerHeight + document.documentElement.scrollTop + scrollThreshold >= 
        document.documentElement.offsetHeight && 
        !loading
      ) {
        loadAllEvents();
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loadAllEvents, loading, initialLoad]);

  return (
    <div className="app">
      <h1>Eventos</h1>
      <div className="cards-container">
        {allEvents.map((event, index) => (
          <Card key={`${event.url}-${index}`} event={event} />
        ))}
      </div>
      {loading && <div className="loading">Carregando...</div>}
      {!hasMore && <div className="no-more">Não há mais eventos.</div>}
    </div>
  );
}

export default App;