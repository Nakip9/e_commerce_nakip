import { useMemo, useState } from 'react';
import { useSelector } from 'react-redux';

export function useSearch() {
  const [query, setQuery] = useState('');
  const products = useSelector((state) => state.catalog.products);

  const filteredItems = useMemo(() => {
    if (!query) {
      return products;
    }
    const normalized = query.toLowerCase();
    return products.filter((product) =>
      [product.name, product.description, product.sku]
        .filter(Boolean)
        .some((field) => field.toLowerCase().includes(normalized))
    );
  }, [products, query]);

  return { query, setQuery, filteredItems };
}
