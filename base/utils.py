from .models import Project  # Import the Project model if it's not already imported

def generate_task_change_action(old_task, updated_task):
    """
    This function takes in the old and updated task instances and generates a human-readable
    string that describes what changed in the task.

    :param old_task: The task instance before the update (old state)
    :param updated_task: The task instance after the update (new state)
    :return: A human-readable string describing the changes
    """
    changes = []

    # Ensure all fields are strings and strip any extra spaces or normalize them
    old_title = str(old_task.get('title', '')).strip()
    updated_title = str(updated_task.get('title', '')).strip()
    
    old_body = str(old_task.get('body', '')).strip()
    updated_body = str(updated_task.get('body', '')).strip()
    
    old_duration = old_task.get('duration', None)
    updated_duration = updated_task.get('duration', None)
    
    old_drafted = old_task.get('drafted', False)
    updated_drafted = updated_task.get('drafted', False)
    
    old_project_id = old_task.get('project', None)  # Get the project ID from old task
    updated_project_id = updated_task.get('project', None)  # Get the project ID from updated task

    # Fetch project names if IDs are provided
    old_project_name = ''
    updated_project_name = ''
    if old_project_id:
        old_project = Project.objects.filter(id=old_project_id).first()
        old_project_name = old_project.name if old_project else "Unknown project"
    
    if updated_project_id:
        updated_project = Project.objects.filter(id=updated_project_id).first()
        updated_project_name = updated_project.name if updated_project else "Unknown project"

    # Compare and generate the action details for each field
    if old_title != updated_title:
        changes.append(f"The task title was changed from '{old_title}' to '{updated_title}'")

    if old_body != updated_body:
        changes.append(f"The task body was updated.")

    if old_duration != updated_duration:
        changes.append(f"The task duration was updated from {old_duration} to {updated_duration} minutes.")

    if old_drafted != updated_drafted:
        drafted_status_old = 'Draft' if old_drafted else 'Published'
        drafted_status_new = 'Draft' if updated_drafted else 'Published'
        changes.append(f"The task drafted status was changed from '{drafted_status_old}' to '{drafted_status_new}'.")

    # Handle the project change case
    if old_project_id != updated_project_id:
        if old_project_id is None:  # Project was previously empty
            changes.append(f"The task project was just set to '{updated_project_name}'.")
        else:
            if updated_project_id:
                changes.append(f"The task project was changed from '{old_project_name}' to '{updated_project_name}'")
            else:
                changes.append(f"The task was unassigned from the project '{old_project_name}'.")

    # If no changes detected, return a default message
    if not changes:
        return "No changes detected."

    # Join all changes into a single string
    action_details = "\n".join(changes)

    return action_details
