import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">UİSBS</h3>
            <p className="text-gray-300 text-sm">
              Ulusal İlaç Stok Takip ve Dağıtım Veri Sistemi - 
              Türkiye'deki tüm eczanelerin ilaç stoklarını merkezi platformda paylaşarak 
              vatandaşların ilaç erişimini kolaylaştıran sistem.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Hızlı Linkler</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/" className="text-gray-300 hover:text-white transition-colors">
                  Ana Sayfa
                </a>
              </li>
              <li>
                <a href="/search" className="text-gray-300 hover:text-white transition-colors">
                  İlaç Ara
                </a>
              </li>
              <li>
                <a href="/about" className="text-gray-300 hover:text-white transition-colors">
                  Hakkımızda
                </a>
              </li>
              <li>
                <a href="/contact" className="text-gray-300 hover:text-white transition-colors">
                  İletişim
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">İletişim</h3>
            <div className="text-gray-300 text-sm space-y-2">
              <p>T.C. Sağlık Bakanlığı</p>
              <p>Bilgi İşlem Dairesi Başkanlığı</p>
              <p>Email: info@uisbs.gov.tr</p>
              <p>Tel: +90 312 XXX XX XX</p>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-300 text-sm">
            © 2024 UİSBS - Tüm hakları saklıdır. T.C. Sağlık Bakanlığı
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 