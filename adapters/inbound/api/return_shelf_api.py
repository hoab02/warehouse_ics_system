@router.post("/{execution_task_id}/return")
def return_shelf(
    execution_task_id: str,
    use_case: ReturnShelfUseCase = Depends(get_return_shelf_uc),
):
    use_case.execute(execution_task_id)
    return {"status": "RETURN_TRIGGERED"}
