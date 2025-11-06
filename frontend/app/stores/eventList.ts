export const useActivityStore = defineStore('activity', () => {
  const listOfActivities = [
    "FTC Robotics",
    "Town Hall Meeting",
    "Science Fair",
    "Math Olympiad",
    "Art Exhibition",
    "Debate Club",
    "Photography Club",
    "Music Rehearsal",
    "Swimming Practice",
    "Football Practice",
  ];
  const activities = ref([...listOfActivities]);
  return {
    activities
  };
});
