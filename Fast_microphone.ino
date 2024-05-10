void setup() {
  Serial.begin(115200);
  // Установка предделителя АЦП на 16 (более быстрая частота дискретизации)
  ADCSRA |= (1 << ADPS2);
  ADCSRA &= ~(1 << ADPS1) & ~(1 << ADPS0);
}

void loop() {
  int sensorValue = analogRead(A0); // Чтение с аналогового пина A0
  Serial.println(sensorValue); // Отправка значения на компьютер
  delayMicroseconds(100); // Задержка для контроля частоты дискретизации
}
