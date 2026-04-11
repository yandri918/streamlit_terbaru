/**
 * TaxPro API Integration for React Native Mobile App
 */

import axios from 'axios';

const API_BASE = 'http://your-api-server.com'; // Change to your API URL
const API_KEY = 'your-api-key'; // Your API key

// ============================================================================
// API Client
// ============================================================================

class TaxProAPI {
    static async request(endpoint, method = 'POST', data = null) {
        try {
            const config = {
                method,
                url: `${API_BASE}${endpoint}`,
                headers: {
                    'X-API-Key': API_KEY,
                    'Content-Type': 'application/json',
                },
            };

            if (data) {
                if (method === 'GET') {
                    config.params = data;
                } else {
                    config.data = data;
                }
            }

            const response = await axios(config);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.error?.message || error.message);
        }
    }

    // Tax Calculations
    static async calculatePPh21(data) {
        return this.request('/api/v1/tax/pph21', 'POST', data);
    }

    static async calculatePPh23(data) {
        return this.request('/api/v1/tax/pph23', 'POST', data);
    }

    static async calculatePPN(data) {
        return this.request('/api/v1/tax/ppn', 'POST', data);
    }

    static async calculatePPhBadan(data) {
        return this.request('/api/v1/tax/pph-badan', 'POST', data);
    }

    static async calculatePBB(data) {
        return this.request('/api/v1/tax/pbb', 'POST', data);
    }

    static async calculatePKB(data) {
        return this.request('/api/v1/tax/pkb', 'POST', data);
    }

    static async calculateBPHTB(data) {
        return this.request('/api/v1/tax/bphtb', 'POST', data);
    }

    // Dashboard
    static async getDashboardSummary(startDate, endDate) {
        return this.request('/api/v1/dashboard/summary', 'GET', {
            start_date: startDate,
            end_date: endDate,
        });
    }

    // AI Advisor
    static async askAIAdvisor(question, context = null) {
        return this.request('/api/v1/ai/advisor', 'POST', {
            question,
            context,
        });
    }
}

// ============================================================================
// React Native Component Example
// ============================================================================

import React, { useState } from 'react';
import {
    View,
    Text,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    ActivityIndicator,
    Alert,
} from 'react-native';

const PPh21Calculator = () => {
    const [gajiPokok, setGajiPokok] = useState('');
    const [tunjangan, setTunjangan] = useState('');
    const [statusKawin, setStatusKawin] = useState('K/1');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleCalculate = async () => {
        if (!gajiPokok) {
            Alert.alert('Error', 'Gaji pokok harus diisi');
            return;
        }

        setLoading(true);
        try {
            const response = await TaxProAPI.calculatePPh21({
                gaji_pokok: parseFloat(gajiPokok),
                tunjangan: parseFloat(tunjangan) || 0,
                status_kawin: statusKawin,
            });

            if (response.status === 'success') {
                setResult(response.data);
            }
        } catch (error) {
            Alert.alert('Error', error.message);
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (value) => {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
        }).format(value);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Kalkulator PPh 21</Text>

            <TextInput
                style={styles.input}
                placeholder="Gaji Pokok"
                keyboardType="numeric"
                value={gajiPokok}
                onChangeText={setGajiPokok}
            />

            <TextInput
                style={styles.input}
                placeholder="Tunjangan"
                keyboardType="numeric"
                value={tunjangan}
                onChangeText={setTunjangan}
            />

            <TextInput
                style={styles.input}
                placeholder="Status Kawin (K/1)"
                value={statusKawin}
                onChangeText={setStatusKawin}
            />

            <TouchableOpacity
                style={styles.button}
                onPress={handleCalculate}
                disabled={loading}
            >
                {loading ? (
                    <ActivityIndicator color="#fff" />
                ) : (
                    <Text style={styles.buttonText}>Hitung Pajak</Text>
                )}
            </TouchableOpacity>

            {result && (
                <View style={styles.resultContainer}>
                    <Text style={styles.resultTitle}>Hasil Perhitungan:</Text>
                    <View style={styles.resultRow}>
                        <Text style={styles.resultLabel}>Penghasilan Bruto:</Text>
                        <Text style={styles.resultValue}>
                            {formatCurrency(result.penghasilan_bruto)}
                        </Text>
                    </View>
                    <View style={styles.resultRow}>
                        <Text style={styles.resultLabel}>PTKP:</Text>
                        <Text style={styles.resultValue}>
                            {formatCurrency(result.ptkp)}
                        </Text>
                    </View>
                    <View style={styles.resultRow}>
                        <Text style={styles.resultLabel}>PKP:</Text>
                        <Text style={styles.resultValue}>
                            {formatCurrency(result.pkp)}
                        </Text>
                    </View>
                    <View style={[styles.resultRow, styles.totalRow]}>
                        <Text style={styles.totalLabel}>Pajak Bulanan:</Text>
                        <Text style={styles.totalValue}>
                            {formatCurrency(result.pajak_bulanan)}
                        </Text>
                    </View>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: '#f5f5f5',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        color: '#333',
    },
    input: {
        backgroundColor: '#fff',
        borderRadius: 8,
        padding: 15,
        marginBottom: 15,
        borderWidth: 1,
        borderColor: '#ddd',
    },
    button: {
        backgroundColor: '#007AFF',
        borderRadius: 8,
        padding: 15,
        alignItems: 'center',
        marginTop: 10,
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: 'bold',
    },
    resultContainer: {
        backgroundColor: '#fff',
        borderRadius: 8,
        padding: 20,
        marginTop: 20,
    },
    resultTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 15,
        color: '#333',
    },
    resultRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: 8,
        borderBottomWidth: 1,
        borderBottomColor: '#eee',
    },
    resultLabel: {
        fontSize: 14,
        color: '#666',
    },
    resultValue: {
        fontSize: 14,
        fontWeight: '600',
        color: '#333',
    },
    totalRow: {
        marginTop: 10,
        paddingTop: 15,
        borderTopWidth: 2,
        borderTopColor: '#007AFF',
        borderBottomWidth: 0,
    },
    totalLabel: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#007AFF',
    },
    totalValue: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#007AFF',
    },
});

export default PPh21Calculator;
export { TaxProAPI };
