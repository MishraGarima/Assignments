/*TDB Assignment 4: 3-way external Merge Sort*/

// C++ program to implement external sorting using merge sort
#include <bits/stdc++.h>
using namespace std;

struct MinHeapNode 
{
	int element;            // The element to be stored
    int i;                  // index of the array from which the element is taken
};

// Prototype of a utility function to swap two min heap nodes
void swap(MinHeapNode* x, MinHeapNode* y);

class MinHeap               // A class for Min Heap
{
	MinHeapNode* harr;      // pointer to array of elements in heap
	int heap_size;          // size of min heap
    public:
        MinHeap(MinHeapNode a[], int size);     // Constructor: creates a min heap of given size
	    void MinHeapify(int);              // to heapify a subtree with root at given index
    	int left(int i) { return (2 * i + 1); }     // to get index of left child of node at index i
        int right(int i) { return (2 * i + 2); }    // to get index of right child of node at index i
        MinHeapNode getMin() { return harr[0]; }    // to get the root
        void replaceMin(MinHeapNode x)      // to replace root with new node x and heapify() new root
	    {
		    harr[0] = x;
		    MinHeapify(0);
	    }
};

MinHeap::MinHeap(MinHeapNode a[], int size)     // Constructor: Builds a heap from a given array a[] of given size
{
	heap_size = size;
	harr = a;                   // store address of array
	int i = (heap_size - 1) / 2;
	while (i >= 0) 
	{
		MinHeapify(i);
		i--;
	}
}

// A recursive method to heapify a subtree with root at given index. This method assumes that the subtrees are already heapified
void MinHeap::MinHeapify(int i)
{
	int l = left(i);
	int r = right(i);
	int smallest = i;
	if (l < heap_size && harr[l].element < harr[i].element)
		smallest = l;
	if (r < heap_size && harr[r].element < harr[smallest].element)
		smallest = r;
	if (smallest != i)
	{
		swap(&harr[i], &harr[smallest]);
		MinHeapify(smallest);
	}
}

void swap(MinHeapNode* x, MinHeapNode* y)       // function to swap two elements
{
	MinHeapNode temp = *x;
	*x = *y;
	*y = temp;
}

void merge(int arr[], int l, int m, int r)      // Merges two subarrays of arr[]. First subarray is arr[l..m] Second subarray is arr[m+1..r]
{
	int i, j, k;
	int n1 = m - l + 1;
	int n2 = r - m;
	int L[n1], R[n2];           // create temp arrays
	for (i = 0; i < n1; i++)    // Copy data to temp arrays L[] and R[]
		L[i] = arr[l + i];
	for (j = 0; j < n2; j++)
		R[j] = arr[m + 1 + j];
	//Merge the temp arrays back into arr[l..r]
	i = 0;                      // Initial index of first subarray
	j = 0;                      // Initial index of second subarray
	k = l;                      // Initial index of merged subarray
	while (i < n1 && j < n2)
	{
		if (L[i] <= R[j])
			arr[k++] = L[i++];
		else
			arr[k++] = R[j++];
	}
	while (i < n1)              // Copy the remaining elements of L[], if there are any
		arr[k++] = L[i++];
	while (j < n2)              // Copy the remaining elements of R[], if there are any
		arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r)     // l is for left index and r is right index of the sub-array of arr to be sorted
{
	if (l < r)
	{
		int m = l + (r - l) / 2;            // Same as (l+r)/2, but avoids overflow for large l and h
		// Sort first and second halves
		mergeSort(arr, l, m);
		mergeSort(arr, m + 1, r);
		merge(arr, l, m, r);
	}
}

FILE* openFile(char* fileName, char* mode)
{
	FILE* fp = fopen(fileName, mode);
	if (fp == NULL)
	{
		perror("Error while opening the file.\n");
		exit(EXIT_FAILURE);
	}
	return fp;
}

void mergeFiles(char* output_file, int n, int k)    // Merges k sorted files. Names of files are assumed to be 1, 2, 3, ... k
{
	FILE* in[k];
	for (int i = 0; i < k; i++)
	{
		char fileName[2];
		snprintf(fileName, sizeof(fileName),"%d", i);   // convert i to string
		in[i] = openFile(fileName, "r");                // Open output files in read mode.
	}
	FILE* out = openFile(output_file, "w");             // FINAL OUTPUT FILE
	// Create a min heap with k heap nodes. Every heap node has first element of scratch output file
	MinHeapNode* harr = new MinHeapNode[k];
	int i;
	for (i = 0; i < k; i++) 
	{
		if (fscanf(in[i], "%d ", &harr[i].element) != 1)    // break if no output file is empty and index i will be no. of input files
			break;
		harr[i].i = i;                  // Index of scratch output file
	}
	MinHeap hp(harr, i);                // Create the heap
	int count = 0;
	while (count != i)
	{
		MinHeapNode root = hp.getMin(); // Get the minimum element and store it in output file
		fprintf(out, "%d ", root.element);
		// Find the next element that will replace current root of heap. The next element belongs to same input file as the current min element.
		if (fscanf(in[root.i], "%d ",&root.element)!= 1)
		{
			root.element = INT_MAX;
			count++;
		}
		hp.replaceMin(root);            // Replace root with next element of input file
	}
	for (int i = 0; i < k; i++)         // close input and output files
		fclose(in[i]);
	fclose(out);
}

// Using a merge-sort algorithm, create the initial runs and divide them evenly among the output files
void createInitialRuns(char* input_file, int run_size,int num_ways)
{
	FILE* in = openFile(input_file, "r");   // For big input file
	FILE* out[num_ways];                // output scratch files
	char fileName[2];
	for (int i = 0; i < num_ways; i++)
	{
		snprintf(fileName, sizeof(fileName),"%d", i);   // convert i to string
		out[i] = openFile(fileName, "w");           // Open output files in write mode.
	}
	// allocate a dynamic array large enough to accommodate runs of size run_size
	int* arr = (int*)malloc(run_size * sizeof(int));
	bool more_input = true;
	int next_output_file = 0;
	int i;
	while (more_input) 
	{
		for (i = 0; i < run_size; i++)      // write run_size elements into arr from input file
		{
			if (fscanf(in, "%d ", &arr[i]) != 1)
			{
				more_input = false;
				break;
			}
		}
		mergeSort(arr, 0, i - 1);           // sort array using merge sort
		for (int j = 0; j < i; j++)
			fprintf(out[next_output_file],"%d ", arr[j]);
		next_output_file++;
	}
	for (int i = 0; i < num_ways; i++)      // close input and output files
		fclose(out[i]);

	fclose(in);
}

// For sorting data stored on disk
void externalSort(char* input_file, char* output_file,int num_ways, int run_size)
{
	createInitialRuns(input_file,run_size, num_ways);
	mergeFiles(output_file, run_size, num_ways);    // Merge the runs using the K-way merging
}

int main()
{
	int num_ways = 10;                      // No. of Partitions of input file.
	int run_size = 3;                    // The size of each partition
	char input_file[] = "input.txt";
	char output_file[] = "output.txt";
	FILE* in = openFile(input_file, "w");
	srand(time(NULL));
	for (int i = 0; i < num_ways * run_size; i++)           // generate input
		fprintf(in, "%d ", rand());

	fclose(in);

	externalSort(input_file, output_file, num_ways,run_size);
	return 0;
}
