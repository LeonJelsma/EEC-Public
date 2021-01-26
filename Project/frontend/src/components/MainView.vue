<template>
  <div>
    <select @change="onUpdateRoom" v-model="selectedRoom">
      <option v-for="room in rooms" :value="room" :key="room.id"> {{ room.name }}</option>
    </select>
    <select @change="onUpdateSensor" :disabled="sensors == null || sensors.length < 1" v-model="selectedSensor">
      <option v-for="sensor in sensors" :value="sensor" :key="sensor.name"> {{ sensor.name }}</option>
    </select>
    <div v-if="selectedSensor != null && selectedSensor.type == 1">
      <MeasurementChart :chart-data="getTempMeasurements(selectedSensor.id)" class="small"></MeasurementChart>
    </div>
  </div>
</template>

<script>
import Axios from "axios-observable";
import MeasurementChart from "@/components/MeasurementChart";

export default {
  name: "MainView",
  components: {MeasurementChart},
  mounted() {
    this.getRooms().subscribe(x => {
      this.rooms = x.data
      this.selectedRoom = x.data[0]
    })
  },
  data() {
    return {
      apiUrl: "http://" + window.location.host.split(':')[0] + ":8000/api/",
      rooms: null,
      sensors: null,
      selectedRoom: null,
      selectedSensor: null,
      chartData:
        {
          label: 'Data One',
          backgroundColor: '#f87979',
          data: []
        },
    }
  },
  computed: {},
  methods: {
    onUpdateRoom() {
      this.getSensors(this.selectedRoom.id).subscribe(x => {
        console.log(x.data)
        this.sensors = x.data
      })
    },
    onUpdateSensor() {
      this.getTempMeasurements(this.selectedSensor.id).subscribe(x => {
        const data = {
          x: [],
          y: []
        }
        for (let point in x.data) {
          console.log(x.data[point])
          data.x.concat(x.data[point].temperature)
          data.y.concat(x.data[point].timestamp)
        }
        return data
      })
    },
    getRooms() {
      return Axios.get(this.apiUrl + 'rooms/')
    },
    getSensors(roomId = -1) {
      let arg = ""
      if (roomId != -1) {
        arg = "?room_id=" + String(roomId)
      }
      return Axios.get(this.apiUrl + 'sensors/' + arg)
    },
    getTempMeasurements(sensorId = -1) {
      let arg = ""
      if (sensorId != -1) {
        arg = "?sensor_id=" + String(sensorId)
      }
      return Axios.get(this.apiUrl + 'temperature_measurements/' + arg)
    }
  }
}
</script>

<style scoped>
.small {
  max-width: 600px;
  margin: 150px auto;
}
</style>