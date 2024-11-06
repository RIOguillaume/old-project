package model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class GridTest {
    private Grid grid;
    @BeforeEach
    void setUp() {
        grid = new Grid(3,3);
    }


    @Test
    void getNeighbours() {
        List<Cell> listOfCells = grid.getNeighbours(1,1);
        assertEquals(8,listOfCells.size());
        assertTrue(listOfCells.contains(grid.getCell(0,0)));
        assertTrue(listOfCells.contains(grid.getCell(0,1)));
        assertTrue(listOfCells.contains(grid.getCell(0,2)));
        assertTrue(listOfCells.contains(grid.getCell(2,0)));
        assertTrue(listOfCells.contains(grid.getCell(2,1)));
        assertTrue(listOfCells.contains(grid.getCell(2,2)));
        assertTrue(listOfCells.contains(grid.getCell(1,0)));
        assertTrue(listOfCells.contains(grid.getCell(1,2)));
    }

    @Test
    void countAliveNeighbours() {
        assertEquals(0,grid.countAliveNeighbours(0,0));
        grid.getCell(1,1).setState(CellState.ALIVE);
        assertEquals(1,grid.countAliveNeighbours(0,0));
        grid.getCell(0,1).setState(CellState.ALIVE);
        assertEquals(2,grid.countAliveNeighbours(0,0));
        grid.getCell(0,2).setState(CellState.ALIVE);
        assertEquals(3,grid.countAliveNeighbours(0,0));
    }

    @Test
    void calculateNextState() {
        assertEquals(CellState.DEAD,grid.calculateNextState(0,0));
        grid.getCell(1,0).setState(CellState.ALIVE);
        assertEquals(CellState.DEAD,grid.calculateNextState(0,0));
        grid.getCell(0,1).setState(CellState.ALIVE);
        assertEquals(CellState.DEAD,grid.calculateNextState(0,0));
        grid.getCell(1,1).setState(CellState.ALIVE);
        assertEquals(CellState.ALIVE,grid.calculateNextState(0,0));
        assertEquals(CellState.ALIVE,grid.calculateNextState(1,1));
        grid.getCell(1,2).setState(CellState.ALIVE);
        assertEquals(CellState.ALIVE,grid.calculateNextState(1,1));
        grid.getCell(2,1).setState(CellState.ALIVE);
        assertEquals(CellState.DEAD,grid.calculateNextState(1,1));
    }

    @Test
    void calculateNextStates() {
        grid.getCell(0,0).setState(CellState.ALIVE);
        grid.getCell(0,1).setState(CellState.ALIVE);
        grid.getCell(0,2).setState(CellState.ALIVE);
        CellState[][] cellState = grid.calculateNextStates();
        for (int i = 0; i < grid.getNumberOfRows(); i++) {
            for (int j = 0; j < grid.getNumberOfColumns(); j++) {
                assertEquals(CellState.ALIVE,cellState[i][j]);
            }
        }
        for(int i = 0; i< grid.getNumberOfColumns(); i++) {
            grid.getCell(i,0).setState(CellState.ALIVE);
            grid.getCell(i,1).setState(CellState.ALIVE);
	    grid.getCell(i,2).setState(CellState.ALIVE);
        }
        cellState = grid.calculateNextStates();
        for (int i = 0; i < grid.getNumberOfRows(); i++) {
            for (int j = 0; j < grid.getNumberOfColumns(); j++) {
                assertEquals(CellState.DEAD,cellState[i][j]);
            }
        }
    }

    @Test
    void updateStates() {
        grid.getCell(0,0).setState(CellState.ALIVE);
        grid.getCell(0,1).setState(CellState.ALIVE);
        grid.getCell(0,2).setState(CellState.ALIVE);
        grid.updateStates(grid.calculateNextStates());
        for (int i = 0; i < grid.getNumberOfRows(); i++) {
            for (int j = 0; j < grid.getNumberOfColumns(); j++) {
                assertEquals(CellState.ALIVE,grid.getCell(i,j).getState());
            }
        }
    }

    @Test
    void updateToNextGeneration() {
        grid.getCell(0,0).setState(CellState.ALIVE);
        grid.getCell(0,1).setState(CellState.ALIVE);
        grid.getCell(0,2).setState(CellState.ALIVE);
        grid.updateToNextGeneration();
        grid.updateToNextGeneration();
        for (int i = 0; i < grid.getNumberOfRows(); i++) {
            for (int j = 0; j < grid.getNumberOfColumns(); j++) {
                assertEquals(CellState.DEAD,grid.getCell(i,j).getState());
            }
        }
    }

    @Test
    void clear() {
        grid.getCell(0,0).setState(CellState.ALIVE);
        grid.getCell(1,1).setState(CellState.ALIVE);
        grid.getCell(2,1).setState(CellState.ALIVE);
        grid.clear();
        for (int i = 0; i < grid.getNumberOfRows(); i++) {
            for (int j = 0; j < grid.getNumberOfColumns(); j++) {
                assertEquals(CellState.DEAD,grid.getCell(i,j).getState());
            }
        }
    }

/*    @Test
   * void randomGeneration() {
   * }
    *
 */
}
