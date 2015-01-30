from django.db.migrations.operations.base import Operation

class AddAchievementOperation(Operation):
    reduces_to_sql = False
    
    reversible = True
    
    def __init__(self, achievement):
        self.achievement = achievement
    
    def state_forwards(self, app_label, state):
        pass
    
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        Achievement = from_state.render().get_model("achievements", "achievement")
        Achievement.objects.create(id = self.achievement.id,
                                   name = self.achievement.name,
                                   description = self.achievement.description)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        Achievement = from_state.render().get_model("achievements", "achievement")
        Achievement.objects.get(pk = self.achievement.id).delete()

    def describe(self):
        # This is used to describe what the operation does in console output.
        return "Adds an achievement '%s'" %self.achievement.name