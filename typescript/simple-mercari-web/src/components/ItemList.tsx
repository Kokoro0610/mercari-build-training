import { useEffect, useState } from 'react';
import { Item, fetchItems } from '~/api';

// const PLACEHOLDER_IMAGE = import.meta.env.VITE_FRONTEND_URL + '/logo192.png';

interface Prop {
  reload: boolean;
  onLoadCompleted: () => void;
}

export const ItemList = ({ reload, onLoadCompleted }: Prop) => {
  const [items, setItems] = useState<Item[]>([]);
  useEffect(() => {
    const fetchData = () => {
      fetchItems()
        .then((data) => {
          console.debug('GET success:', data);
          setItems(data.items);
          onLoadCompleted();
        })
        .catch((error) => {
          console.error('GET error:', error);
        });
    };

    if (reload) {
      fetchData();
    }
  }, [reload, onLoadCompleted]);

  return (
    <div className="ItemsGrid">
      {items?.map((item) => (
        <div key={item.id} className="ItemList">
          <img
            src={`http://localhost:9000/image/${item.id}.jpg`}
            alt={item.name}
            style={{
              width: "150px",
              height: "150px",
              objectFit: "cover"
            }}
          />
          <p>
            <span>Name: {item.name}</span>
            <br />
            <span>Category: {item.category}</span>
          </p>
        </div>
      ))}
    </div>
  );  
};
