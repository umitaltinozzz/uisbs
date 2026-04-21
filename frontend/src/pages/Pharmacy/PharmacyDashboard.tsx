import React, { useState, useEffect } from 'react';

interface DrugStock {
  id: string;
  barcode: string;
  name: string;
  quantity: number;
  minQuantity: number;
  price: number;
  expiryDate: string;
  manufacturer: string;
}

interface DashboardStats {
  totalDrugs: number;
  lowStockCount: number;
  expiringSoonCount: number;
  totalValue: number;
}

const PharmacyDashboard: React.FC = () => {
  const [stocks, setStocks] = useState<DrugStock[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    totalDrugs: 0,
    lowStockCount: 0,
    expiringSoonCount: 0,
    totalValue: 0
  });
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      // Mock data for now
      const mockStocks: DrugStock[] = [
        {
          id: '1',
          barcode: '8699546334455',
          name: 'Parol 500mg',
          quantity: 45,
          minQuantity: 20,
          price: 15.50,
          expiryDate: '2024-12-31',
          manufacturer: 'Atabay'
        },
        {
          id: '2',
          barcode: '8699546334456',
          name: 'Aspirin 100mg',
          quantity: 8,
          minQuantity: 15,
          price: 12.75,
          expiryDate: '2024-06-15',
          manufacturer: 'Bayer'
        }
      ];

      setStocks(mockStocks);
      
      // Calculate stats
      const totalDrugs = mockStocks.length;
      const lowStockCount = mockStocks.filter(stock => stock.quantity <= stock.minQuantity).length;
      const expiringSoonCount = mockStocks.filter(stock => {
        const expiryDate = new Date(stock.expiryDate);
        const threeMonthsFromNow = new Date();
        threeMonthsFromNow.setMonth(threeMonthsFromNow.getMonth() + 3);
        return expiryDate <= threeMonthsFromNow;
      }).length;
      const totalValue = mockStocks.reduce((sum, stock) => sum + (stock.quantity * stock.price), 0);

      setStats({
        totalDrugs,
        lowStockCount,
        expiringSoonCount,
        totalValue
      });
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getStockStatus = (stock: DrugStock) => {
    if (stock.quantity <= stock.minQuantity) {
      return { status: 'Düşük Stok', color: 'text-red-600 bg-red-100' };
    }
    if (stock.quantity <= stock.minQuantity * 1.5) {
      return { status: 'Orta Stok', color: 'text-yellow-600 bg-yellow-100' };
    }
    return { status: 'Yeterli Stok', color: 'text-green-600 bg-green-100' };
  };

  const isExpiringSoon = (expiryDate: string) => {
    const expiry = new Date(expiryDate);
    const threeMonthsFromNow = new Date();
    threeMonthsFromNow.setMonth(threeMonthsFromNow.getMonth() + 3);
    return expiry <= threeMonthsFromNow;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">
              Eczane Yönetim Paneli
            </h1>
            <button
              onClick={() => setShowAddModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Yeni İlaç Ekle
            </button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Toplam İlaç</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.totalDrugs}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-red-100 text-red-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Düşük Stok</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.lowStockCount}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Yakında Bitecek</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.expiringSoonCount}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center">
                <div className="p-3 rounded-full bg-green-100 text-green-600">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Toplam Değer</p>
                  <p className="text-2xl font-semibold text-gray-900">{stats.totalValue.toFixed(2)} ₺</p>
                </div>
              </div>
            </div>
          </div>

          {/* Stock Table */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-800">İlaç Stokları</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      İlaç Bilgileri
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Stok Durumu
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fiyat
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Son Kullanma
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      İşlemler
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stocks.map((stock) => {
                    const stockStatus = getStockStatus(stock);
                    return (
                      <tr key={stock.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900">{stock.name}</div>
                            <div className="text-sm text-gray-500">Barkod: {stock.barcode}</div>
                            <div className="text-sm text-gray-500">{stock.manufacturer}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-gray-900 mr-2">
                              {stock.quantity} adet
                            </span>
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${stockStatus.color}`}>
                              {stockStatus.status}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {stock.price.toFixed(2)} ₺
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`text-sm ${isExpiringSoon(stock.expiryDate) ? 'text-red-600 font-medium' : 'text-gray-900'}`}>
                            {new Date(stock.expiryDate).toLocaleDateString('tr-TR')}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-blue-600 hover:text-blue-900 mr-3">
                            Düzenle
                          </button>
                          <button className="text-red-600 hover:text-red-900">
                            Sil
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Add Modal Placeholder */}
      {showAddModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <h3 className="text-lg font-medium text-gray-900">Yeni İlaç Ekle</h3>
              <p className="text-sm text-gray-500 mt-2">Bu özellik yakında eklenecek...</p>
              <div className="items-center px-4 py-3">
                <button
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 bg-gray-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-300"
                >
                  Kapat
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PharmacyDashboard; 