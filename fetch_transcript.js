// Menggunakan library bawaan Node.js untuk menulis file
const fs = require('fs');

// Fungsi otomatis untuk mengambil transkrip
async function ambilTranskrip(videoId, namaPakar) {
  console.log(`Sedang mengambil transkrip untuk video: ${videoId}...`);
  
  // Kita menggunakan API gratis/uji coba dari Supadata (contoh struktur)
  const urlAPI = `https://api.supadata.ai/v1/youtube/transcript?videoId=${videoId}`;
  
  try {
    const response = await fetch(urlAPI, {
      method: 'GET',
      headers: {
        // Nanti di sini diisi API Key jika kamu sudah mendaftar di Supadata
        'x-api-key': 'MOCK_API_KEY_KAMU' 
      }
    });

    // Jika berhasil, simpan teksnya ke dalam folder youtube-transcripts
    const folderTujuan = `./research/youtube-transcripts/${namaPakar}`;
    
    // Membuat folder khusus nama pakar jika belum ada
    if (!fs.existsSync(folderTujuan)){
        fs.mkdirSync(folderTujuan, { recursive: true });
    }

    // Simulasi menyimpan teks transkrip (nanti diganti data asli dari API)
    const teksTranskrip = `Ini adalah isi transkrip otomatis untuk video ID: ${videoId} milik pakar ${namaPakar}.`;
    
    fs.writeFileSync(`${folderTujuan}/${videoId}.txt`, teksTranskrip);
    console.log(`✅ Berhasil! File disimpan di: ${folderTujuan}/${videoId}.txt`);

  } catch (error) {
    console.error("Waduh, ada yang error saat ambil data:", error);
  }
}

// Menjalankan fungsi di atas untuk contoh video Pakar "tk-kader"
// Gantilah 'dQw4w9WgXcQ' dengan ID video YouTube aslinya nanti
ambilTranskrip('dQw4w9WgXcQ', 'tk-kader');