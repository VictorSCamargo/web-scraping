import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Card from './components/Card';

function App() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [initialLoad, setInitialLoad] = useState(false);

  const loadCards = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    try {
      const response = await fetch('/blueticket.json');
      const allData = await response.json();
      
      // Simulação de paginação
      const itemsPerPage = 5;
      const startIndex = (page - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      const newCards = allData.slice(startIndex, endIndex);

      if (newCards.length === 0) {
        setHasMore(false);
      } else {
        setCards(prevCards => {
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
      if (
        window.innerHeight + document.documentElement.scrollTop + 100 >= 
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
        {cards.map((card, index) => (
          <Card key={`${card.url}-${index}`} event={card} />
        ))}
      </div>
      {loading && <div className="loading">Carregando mais eventos...</div>}
      {!hasMore && cards.length > 0 && <div className="no-more">Não há mais eventos para carregar</div>}
    </div>
  );
}

export default App;