// extra.ts
export function convertTimestampToDate(timestamp: { seconds: { low: number; high: number }; nanos: number }): string {
    const seconds = timestamp.seconds.low; // Toma el valor de seconds
    const milliseconds = seconds * 1000 + Math.floor(timestamp.nanos / 1000000); // Convierte a milisegundos
    const date = new Date(milliseconds); // Crea el objeto Date

    // Formatea la fecha y la hora como desees
    const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // Cambia a true si quieres formato 12 horas
    };

    // Convierte la fecha a cadena con formato separado
    const formattedDate = date.toLocaleString('en-US', options)
        .replace(',', '') // Elimina la coma entre fecha y hora
        .replace(' ', ' - '); // Cambia el espacio entre fecha y hora por un guión

    return formattedDate; // Retorna como cadena
}
