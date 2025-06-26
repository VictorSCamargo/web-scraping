import type { GenericEvent } from "../model/eventos-model";
import Card from "./Card";

interface CardContainerProps {
  events: GenericEvent[];
}

function CardContainer(props: CardContainerProps) {
  const { events } = props;

  return (
    <div className="cards-container">
      {events.map((event, index) => (
        <Card key={`${event.url}-${index}`} event={event} />
      ))}
    </div>
  );
}

export default CardContainer;
