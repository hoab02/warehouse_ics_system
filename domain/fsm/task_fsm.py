from enum import Enum
from domain.exceptions import InvalidStateTransition


class TaskStatus(str, Enum):
    PENDING = "PENDING"  # Bổ sung trạng thái FAILED, ưu tiên chạy lại trước.
    DISPATCHED = "DISPATCHED"
    MOVING = "MOVING"
    AT_STATION = "AT_STATION"
    WAITING_RETURN = "WAITING_RETURN"
    RETURNING = "RETURNING"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


ALLOWED_TRANSITIONS = {
    TaskStatus.PENDING: {TaskStatus.DISPATCHED},
    TaskStatus.DISPATCHED: {TaskStatus.MOVING},
    TaskStatus.MOVING: {TaskStatus.AT_STATION},
    TaskStatus.AT_STATION: {TaskStatus.WAITING_RETURN},
    TaskStatus.WAITING_RETURN: {TaskStatus.RETURNING},
    TaskStatus.RETURNING: {TaskStatus.DONE},
}


def validate_transition(current: TaskStatus, target: TaskStatus):
    """
    Kiểm tra xem từ trạng thái hiện tại (current)
    có được phép chuyển sang trạng thái mới (target) hay không

    Raises:
        InvalidStateTransition: nếu chuyển trạng thái không được phép
    """
    # Lấy tập hợp các trạng thái được phép chuyển tới từ current
    # Nếu current không có trong dict → trả về set rỗng
    allowed_targets = ALLOWED_TRANSITIONS.get(current, set())

    # Nếu target KHÔNG nằm trong tập hợp được phép → raise exception
    if target not in allowed_targets:
        raise InvalidStateTransition(
            f"Chuyển trạng thái không hợp lệ: {current} → {target} không được phép"
        )
