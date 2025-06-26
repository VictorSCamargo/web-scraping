import { useState } from "react";
import "../css/App.css";

interface PaginationProps {
  eventsPerPage: number;
  totalEvents: number;
  paginate: (pageNumber: number) => void;
}

function Pagination({ eventsPerPage, totalEvents, paginate }: PaginationProps) {
  const [activePage, setActivePage] = useState(1);
  const totalPages = Math.ceil(totalEvents / eventsPerPage);

  const handlePageChange = (pageNumber: number) => {
    setActivePage(pageNumber);
    paginate(pageNumber);
  };

  const handlePrevious = () => {
    if (activePage > 1) {
      handlePageChange(activePage - 1);
    }
  };

  const handleNext = () => {
    if (activePage < totalPages) {
      handlePageChange(activePage + 1);
    }
  };

  return (
    <div className="pagination-container">
      <button
        className="pagination-return-btn"
        onClick={handlePrevious}
        disabled={activePage === 1}
        style={{
          cursor: activePage === 1 ? "default" : "pointer",
          opacity: activePage === 1 ? 0.3 : 1,
        }}
      >
        &#8249; {/* ← Chevron Left */}
      </button>

      <span className="pagination-current-page-span">
        {activePage} of {totalPages}
      </span>

      <button
        className="pagination-next-btn"
        onClick={handleNext}
        disabled={activePage === totalPages}
        style={{
          cursor: activePage === totalPages ? "default" : "pointer",
          opacity: activePage === totalPages ? 0.3 : 1,
        }}
      >
        &#8250; {/* → Chevron Right */}
      </button>
    </div>
  );
}

export default Pagination;
