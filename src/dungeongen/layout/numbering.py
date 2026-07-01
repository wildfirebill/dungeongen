"""Room numbering using longest-path-first DFS.

Numbers rooms via depth-first traversal. At each junction, the algorithm
visits the exit leading to the largest unvisited subgraph first. This
naturally follows the main spine (the longest path through the dungeon)
and numbers side branches as short detours off the spine. Consecutive
room numbers stay spatially close, minimizing backtracking.
"""

from typing import Dict, Set, List, Tuple, Optional
from .models import Dungeon


def number_dungeon(dungeon: Dungeon, entrance_room_id: Optional[str] = None,
                   spine_direction: Optional[Tuple[float, float]] = None) -> Dict[str, int]:
    """
    Number rooms via longest-path-first DFS.

    Args:
        dungeon: The dungeon to number
        entrance_room_id: Room connected to entrance passage (auto-detected if None)
        spine_direction: Ignored (kept for API compatibility)

    Returns:
        Dict mapping room_id -> room number (1-based)
    """
    graph = _build_adjacency_graph(dungeon)

    if not graph:
        return {}

    if entrance_room_id is None:
        entrance_room_id = _find_entrance_room(dungeon)

    if entrance_room_id is not None and entrance_room_id in graph:
        numbers = _number_dfs(graph, entrance_room_id)
    else:
        numbers = _number_dfs_by_components(graph)

    # Number any rooms not reached (shouldn't happen, but be safe)
    numbers = _fill_unvisited(graph, numbers)

    return numbers


def _build_adjacency_graph(dungeon: Dungeon) -> Dict[str, Set[str]]:
    """Build undirected adjacency graph from room-to-room passages."""
    graph: Dict[str, Set[str]] = {rid: set() for rid in dungeon.rooms.keys()}

    for passage in dungeon.passages.values():
        start = passage.start_room
        end = passage.end_room
        if start is None or end == "passage":
            continue
        if start in graph and end in graph:
            graph[start].add(end)
            graph[end].add(start)

    return graph


def _find_entrance_room(dungeon: Dungeon) -> Optional[str]:
    """Find the first room connected to the entrance passage."""
    for passage in dungeon.passages.values():
        if not passage.start_room:
            if passage.end_room and passage.end_room != "passage":
                return passage.end_room
    return None


# ─── DFS numbering ─────────────────────────────────────────────

def _component_size(graph: Dict[str, Set[str]],
                    start: str,
                    blocked: str,
                    visited: Set[str]) -> int:
    """Count nodes reachable from *start* without passing through *blocked*
    or any already-visited node.  Uses iterative DFS."""
    seen: Set[str] = set()
    stack = [start]
    while stack:
        x = stack.pop()
        if x == blocked or x in visited or x in seen:
            continue
        seen.add(x)
        for y in graph.get(x, []):
            if y != blocked and y not in visited and y not in seen:
                stack.append(y)
    return len(seen)


def _number_dfs(graph: Dict[str, Set[str]],
                entrance: str) -> Dict[str, int]:
    """
    DFS visitor that picks the largest unvisited subgraph first at every
    junction, yielding spine-first numbers.
    """
    numbers: Dict[str, int] = {}
    visited: Set[str] = set()
    next_num = 1

    def _visit(u: str) -> None:
        nonlocal next_num
        if u in visited:
            return
        visited.add(u)
        numbers[u] = next_num
        next_num += 1

    # Iterative DFS with (node, parent, iterator_index) frames.
    # At each node we sort children by *remaining* component size so
    # the longest path unrolled first.
    stack: List[Tuple[str, Optional[str], int]] = [(entrance, None, 0)]

    while stack:
        u, parent, idx = stack.pop()

        if idx == 0:
            # First visit to this node — assign its number
            _visit(u)

        # Get neighbours excluding parent
        neighbours = [v for v in graph.get(u, []) if v != parent and v not in visited]

        if idx < len(neighbours):
            # We still have children to process; push frame back and push child
            v = neighbours[idx]
            stack.append((u, parent, idx + 1))
            stack.append((v, u, 0))
        # else: all children visited, pop naturally

    # Re-sort children by component-size before starting the *actual* DFS.
    # We rebuild the numbers dict from scratch with the correct order.
    numbers2: Dict[str, int] = {}
    visited2: Set[str] = set()
    next_num2 = 1

    def _visit2(u: str) -> None:
        nonlocal next_num2
        if u in visited2:
            return
        visited2.add(u)
        numbers2[u] = next_num2
        next_num2 += 1

    stack2: List[Tuple[str, Optional[str], int, List[str]]] = [(entrance, None, 0, [])]

    while stack2:
        u, parent, phase, children = stack2.pop()

        if phase == 0:
            _visit2(u)
            # Compute children sorted by component-size (largest first)
            raw = [v for v in graph.get(u, []) if v != parent and v not in visited2]
            sized = [(v, _component_size(graph, v, u, visited2)) for v in raw]
            sized.sort(key=lambda x: -x[1])
            children = [v for v, _ in sized]
            # Push a termination marker, then children in reverse order
            stack2.append((u, parent, 1, children))
            for v in reversed(children):
                stack2.append((v, u, 0, []))
        # phase == 1: all children done, nothing to do

    return numbers2


# ─── Connected-component fallback ──────────────────────────────

def _find_components(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Return all connected components as lists of nodes, largest first."""
    unvisited: Set[str] = set(graph.keys())
    components: List[List[str]] = []
    while unvisited:
        start = next(iter(unvisited))
        comp: List[str] = []
        stack = [start]
        while stack:
            u = stack.pop()
            if u not in unvisited:
                continue
            unvisited.remove(u)
            comp.append(u)
            for v in graph.get(u, []):
                if v in unvisited:
                    stack.append(v)
        components.append(comp)
    components.sort(key=len, reverse=True)
    return components


def _number_dfs_by_components(graph: Dict[str, Set[str]]) -> Dict[str, int]:
    """Number rooms using DFS per connected component, largest component first."""
    numbers: Dict[str, int] = {}
    components = _find_components(graph)
    next_num = 1
    for comp in components:
        comp_nums = _number_dfs(graph, comp[0])
        offset = next_num - 1
        for room_id, num in comp_nums.items():
            numbers[room_id] = num + offset
        next_num += len(comp_nums)
    return numbers


def _fill_unvisited(graph: Dict[str, Set[str]],
                    numbers: Dict[str, int]) -> Dict[str, int]:
    """Assign numbers to any nodes missing from *numbers*."""
    if len(numbers) == len(graph):
        return numbers
    next_num = max(numbers.values(), default=0) + 1
    for node in graph:
        if node not in numbers:
            numbers[node] = next_num
            next_num += 1
    return numbers

