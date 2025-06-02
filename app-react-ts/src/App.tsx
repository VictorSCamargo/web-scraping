import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Card from './components/Card';
import { convertBlueticketEventToGeneric, type BlueticketEvent } from './assets/convertBlueticketEventToGeneric';

function App() {
  const [blueticketEvents, setBlueticketEvents] = useState<BlueticketEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [initialLoad, setInitialLoad] = useState<boolean>(false);

  const loadCards = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    try {
      const response = await fetch('/blueticket.json');
      const allData: BlueticketEvent[] = await response.json();
      
      // Simulação de paginação
      const itemsPerPage = 5;
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      const newCards = allData.slice(startIndex, endIndex);

      if (newCards.length === 0) {
        setHasMore(false);
      } else {
        setBlueticketEvents(prevCards => {
          // Evita duplicação verificando se o card já existe
          const existingIds = new Set(prevCards.map(card => card.url));
          const uniqueNewCards = newCards.filter(card => !existingIds.has(card.url));
          return [...prevCards, ...uniqueNewCards];
        });
        setPage(prevPage => prevPage + 1);
      }
    } catch (error) {
      console.error('Error loading cards:', error);
    } finally {
      setLoading(false);
      setInitialLoad(true);
    }
  }, [page, loading, hasMore]);

  // Carrega os primeiros cards
  useEffect(() => {
    if (!initialLoad) {
      loadCards();
    }
  }, [initialLoad, loadCards]);

  // Configura o observer para rolagem infinita
  useEffect(() => {
    if (!initialLoad) return;

    const handleScroll = () => {
      // Carrega novos cards quando estiver a essa distancia antes do final da página
      const scrollThreshold = 900;
      
      if (
        window.innerHeight + document.documentElement.scrollTop + scrollThreshold >= 
        document.documentElement.offsetHeight && 
        !loading
      ) {
        loadCards();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loadCards, loading, initialLoad]);

  return (
    <div className="app">
      <h1>Eventos</h1>
      <div className="cards-container">
        {blueticketEvents.map((card, index) => (
          <Card key={`${card.url}-${index}`} event={convertBlueticketEventToGeneric(card)} />
        ))}
      </div>
      {loading && <div className="loading">Carregando mais eventos...</div>}
      {!hasMore && blueticketEvents.length > 0 && <div className="no-more">Não há mais eventos para carregar</div>}
    </div>
  );
}

export default App;