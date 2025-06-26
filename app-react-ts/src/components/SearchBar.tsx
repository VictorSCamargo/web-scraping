interface SearchBarProps {
  searchInput: string;
  setSearchInput: (value: string) => void;
  handleSearch: () => void;
}

export const SearchBar = (props: SearchBarProps) => {
  const { searchInput, setSearchInput, handleSearch } = props;

  return (
    <div
      style={{
        display: "flex",
        gap: "12px",
        marginBottom: "24px",
        maxWidth: "500px",
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <input
        type="text"
        value={searchInput}
        placeholder="Buscar pelo nome do evento"
        onChange={(e) => setSearchInput(e.target.value)}
        style={{
          flex: 1,
          padding: "12px 16px",
          fontSize: "16px",
          borderRadius: "8px",
          border: "1.5px solid #ccc",
          boxShadow: "inset 0 1px 3px rgba(0,0,0,0.1)",
          transition: "border-color 0.3s",
        }}
        onFocus={(e) => (e.currentTarget.style.borderColor = "#007BFF")}
        onBlur={(e) => (e.currentTarget.style.borderColor = "#ccc")}
      />

      <button
        onClick={handleSearch}
        style={{
          padding: "12px 24px",
          backgroundColor: "#646cff",
          border: "none",
          borderRadius: "8px",
          color: "white",
          fontWeight: "600",
          fontSize: "16px",
          cursor: "pointer",
          boxShadow: "0 4px 8px rgba(0, 123, 255, 0.3)",
          transition: "background-color 0.3s",
        }}
      >
        Buscar
      </button>
    </div>
  );
};
