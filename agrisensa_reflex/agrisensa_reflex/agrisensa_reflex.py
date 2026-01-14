import reflex as rx

# -----------------------------------------------------------------------------
# 1. STATE (Logika Backend - Pengganti "st.session_state" yang lebih canggih)
# -----------------------------------------------------------------------------
class BankSampahState(rx.State):
    """State management untuk aplikasi Bank Sampah."""
    
    # Database harga standar (Dictionary ini reaktif!)
    prices: dict[str, int] = {
        "Organik/Residu": 200,
        "Kertas (Koran/Kardus)": 2500,
        "Kain (Perca)": 1000,
        "Kaleng (Logam)": 12000,
        "Botol PET (Bersih)": 4500,
        "Plastik Bungkus": 1500,
        "Elektronik (E-Waste)": 15000,
    }

    # Menyimpan input user { "Kertas": 10.5, ... }
    inputs: dict[str, float] = {}

    # -- Computed Vars (Dihitung otomatis tanpa fungsi manual!) --
    
    @rx.var
    def total_income(self) -> float:
        """Menghitung total pendapatan secara real-time."""
        total = 0.0
        for category, weight in self.inputs.items():
            price = self.prices.get(category, 0)
            total += weight * price
        return total

    @rx.var
    def chart_data(self) -> list[dict]:
        """Menyiapkan data untuk grafik otomatis."""
        data = []
        for category, weight in self.inputs.items():
            if weight > 0:
                income = weight * self.prices.get(category, 0)
                data.append({"name": category, "value": income})
        return data

    # -- Event Handlers (Fungsi aksi) --
    
    def set_input(self, category: str, value: str):
        """Update berat sampah saat user mengetik."""
        try:
            val = float(value)
        except ValueError:
            val = 0.0
        self.inputs[category] = val

    def update_price(self, category: str, new_price: str):
        """Update harga pasar secara real-time."""
        try:
            self.prices[category] = int(new_price)
        except ValueError:
            pass


# -----------------------------------------------------------------------------
# 2. UI COMPONENTS (Frontend React rasa Python)
# -----------------------------------------------------------------------------

def revenue_card():
    """Kartu indikator Total Pendapatan yang cantik."""
    return rx.box(
        rx.vstack(
            rx.text("💰 Estimasi Pendapatan", font_size="0.9em", color="white"),
            rx.heading(
                f"Rp {BankSampahState.total_income.to_string()}", 
                font_size="2.5em", 
                color="white"
            ),
            rx.text("*Potensi Emas Hijau AgriSensa", font_size="0.8em", color="#E8F5E9"),
            align_items="center",
            spacing="2",
        ),
        padding="2em",
        border_radius="15px",
        background="linear-gradient(45deg, #43a047, #2e7d32)", # Gradient CSS
        box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1)",
        width="100%",
        margin_bottom="2em",
    )

def input_row(category: str):
    """Baris input interaktif untuk setiap kategori sampah."""
    return rx.hstack(
        rx.box(
            rx.text(category, font_weight="bold", color="#1b5e20"),
            width="30%"
        ),
        rx.box(
            rx.input(
                placeholder="Harga/kg",
                default_value=BankSampahState.prices[category].to_string(),
                on_change=lambda val: BankSampahState.update_price(category, val),
                type="number",
                bg="white",
                border_color="#c8e6c9",
            ),
            width="30%"
        ),
        rx.box(
            rx.input(
                placeholder="Berat (kg)",
                on_change=lambda val: BankSampahState.set_input(category, val),
                type="number",
                bg="white",
                border_color="#c8e6c9",
            ),
            width="30%"
        ),
        width="100%",
        padding="1em",
        border_bottom="1px solid #e0e0e0",
        _hover={"bg": "#f1f8e9"}, # Hover effect native
    )

# -----------------------------------------------------------------------------
# 3. MAIN PAGE LAYOUT
# -----------------------------------------------------------------------------
def index():
    return rx.container(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Bank Sampah Terpadu", color="#2e7d32"),
                spacing="4",
                margin_bottom="2em",
            ),
            
            # Layout Utama: Kiri (Input) & Kanan (Hasil)
            rx.flex(
                # Kolom Kiri: Input Tabel
                rx.box(
                    rx.heading("Input Sampah", size="5", margin_bottom="1em"),
                    rx.vstack(
                        rx.foreach(
                            BankSampahState.prices, # Loop otomatis generate baris
                            lambda item: input_row(item[0])
                        ),
                        width="100%",
                        bg="white",
                        padding="1em",
                        border_radius="10px",
                        box_shadow="lg"
                    ),
                    flex="1",
                    margin_right="2em",
                ),
                
                # Kolom Kanan: Result & Viz
                rx.box(
                    revenue_card(),
                    
                    rx.heading("Analisis Nilai", size="5", margin_bottom="1em"),
                    # Menggunakan Recharts (Library grafik standar React)
                    rx.recharts.pie_chart(
                        rx.recharts.pie(
                            data=BankSampahState.chart_data,
                            data_key="value",
                            name_key="name",
                            cx="50%",
                            cy="50%",
                            fill="#8884d8",
                            label=True,
                        ),
                        width="100%",
                        height=300,
                    ),
                    flex="1",
                ),
                width="100%",
                flex_direction=["column", "column", "row"], # Responsif: HP col, PC row
            ),
        ),
        max_width="1200px",
        padding_y="2em",
        font_family="Inter",
        background_color="#fafafa" # Background page abu-abu sangat muda
    )

# Init App
app = rx.App()
app.add_page(index, title="AgriSensa Bank Sampah")
