import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# posição (linha, coluna) de cada peça no estado objetivo
GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (admissível e consistente)."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            gr, gc = GOAL_POS[tile]
            total += abs(r - gr) + abs(c - gc)
        return total

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        tie = count()                         # desempate estável no heap
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: 0}
        closed = set()

        while frontier:
            _, _, state = heapq.heappop(frontier)

            if state.tiles in closed:
                continue

            if state.is_goal:                 # teste na expansão (garante solução ótima)
                result.solution = state
                result.depth = state.cost
                return result

            closed.add(state.tiles)
            result.nodes_expanded += 1

            for child in state.neighbors():
                if child.tiles in closed:
                    continue
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    heapq.heappush(frontier, (child.cost + self.heuristic(child), next(tie), child))
                    result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
