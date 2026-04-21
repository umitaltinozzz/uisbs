import React, { useState } from 'react';

interface SearchFilters {
  drugName: string;
  location: string;
  radius: number;
  inStock: boolean;
}

const SearchPage: React.FC = () => {
  const [filters, setFilters] = useState<SearchFilters>({
    drugName: '',
    location: '',
    radius: 5,
    inStock: true
  });

  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // API call will be implemented here
      console.log('Searching with filters:', filters);
      // Mock results for now
      setSearchResults([
        {
          id: '1',
          drugName: 'Parol 500mg',
          pharmacyName: 'Merkez Eczanesi',
          address: 'Kızılay, Ankara',
          distance: '0.5 km',
          price: '15.50 TL',
          inStock: true
        }
      ]);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            İlaç Arama
          </h1>

          {/* Search Form */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <form onSubmit={handleSearch} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label htmlFor="drugName" className="block text-sm font-medium text-gray-700 mb-1">
                    İlaç Adı
                  </label>
                  <input
                    type="text"
                    id="drugName"
                    value={filters.drugName}
                    onChange={(e) => setFilters({ ...filters, drugName: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="İlaç adını girin..."
                    required
                  />
                </div>

                <div>
                  <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
                    Konum
                  </label>
                  <input
                    type="text"
                    id="location"
                    value={filters.location}
                    onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Şehir, ilçe..."
                  />
                </div>

                <div>
                  <label htmlFor="radius" className="block text-sm font-medium text-gray-700 mb-1">
                    Yarıçap (km)
                  </label>
                  <select
                    id="radius"
                    value={filters.radius}
                    onChange={(e) => setFilters({ ...filters, radius: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={1}>1 km</option>
                    <option value={5}>5 km</option>
                    <option value={10}>10 km</option>
                    <option value={25}>25 km</option>
                  </select>
                </div>

                <div className="flex items-end">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    {isLoading ? 'Aranıyor...' : 'Ara'}
                  </button>
                </div>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="inStock"
                  checked={filters.inStock}
                  onChange={(e) => setFilters({ ...filters, inStock: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="inStock" className="ml-2 block text-sm text-gray-700">
                  Sadece stokta olanları göster
                </label>
              </div>
            </form>
          </div>

          {/* Search Results */}
          <div className="space-y-4">
            {searchResults.length > 0 && (
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Arama Sonuçları ({searchResults.length})
              </h2>
            )}

            {searchResults.map((result) => (
              <div key={result.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">
                      {result.drugName}
                    </h3>
                    <p className="text-gray-600 mb-1">
                      <span className="font-medium">Eczane:</span> {result.pharmacyName}
                    </p>
                    <p className="text-gray-600 mb-1">
                      <span className="font-medium">Adres:</span> {result.address}
                    </p>
                    <p className="text-gray-600">
                      <span className="font-medium">Mesafe:</span> {result.distance}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-600 mb-2">
                      {result.price}
                    </div>
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      result.inStock 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {result.inStock ? 'Stokta' : 'Stokta Yok'}
                    </span>
                  </div>
                </div>
              </div>
            ))}

            {searchResults.length === 0 && !isLoading && (
              <div className="text-center py-12">
                <div className="text-gray-400 text-lg">
                  Arama yapmak için yukarıdaki formu kullanın
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage; 