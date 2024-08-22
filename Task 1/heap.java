import java.util.Arrays;
import java.util.NoSuchElementException;

public class ExponentialHeap {
    private double exponent;
    private int currentSize;
    private int[] elements;

    // Constructor
    public ExponentialHeap(double exponent, int maxCapacity) {
        this.exponent = exponent;
        this.currentSize = 0;
        this.elements = new int[maxCapacity + 1];
        Arrays.fill(elements, -1);
    }

    private int getParentIndex(int i) {
        return (int) ((i - 1) / Math.pow(2, exponent));
    }

    public boolean isAtCapacity() {
        return currentSize == elements.length;
    }

    public void add(int value) {
        if (isAtCapacity()) {
            throw new NoSuchElementException("Heap is full, cannot insert new element.");
        } else {
            elements[currentSize++] = value;
            adjustUpward(currentSize - 1);
        }
    }

    private void adjustUpward(int i) {
        int temp = elements[i];
        while (i > 0 && temp > elements[getParentIndex(i)]) {
            elements[i] = elements[getParentIndex(i)];
            i = getParentIndex(i);
        }
        elements[i] = temp;
    }

    public int removeMax() {
        if (currentSize == 0) {
            throw new NoSuchElementException("Heap is empty, no element to remove.");
        }

        int maxElement = elements[0];
        elements[0] = elements[currentSize - 1];
        elements[currentSize - 1] = -1;
        currentSize--;

        int i = 0;
        while (i < currentSize - 1) {
            adjustUpward(i);
            i++;
        }

        return maxElement;
    }

    public void display() {
        for (int i = 0; i < currentSize; i++) {
            System.out.print(elements[i]);
            if (i < currentSize - 1) {
                System.out.print(", ");
            }
        }
        System.out.println();
    }

    public static void main(String[] args) {
        double exponentValue = 3;
        int maxCapacity = 15; 

        ExponentialHeap heap = new ExponentialHeap(exponentValue, maxCapacity);
        heap.add(15);
        heap.add(25);
        heap.add(7);
        heap.add(20);
        heap.add(30);

        heap.display();

        int maxElement = heap.removeMax();
        System.out.println("Max element: " + maxElement);

        heap.display();
    }
}
