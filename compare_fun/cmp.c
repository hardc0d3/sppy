#include<stdio.h>


extern int
compare_function(char *a, size_t asz, char *b, size_t bsz, void *arg)
{
	/* compare */
	/* return -1, 0, 1 */ /*? a<b -1 a=b 1 a>b 1*/
size_t a_idx, b_idx;
//int ret = 0;
size_t* start_idx =(size_t *)arg ;
a_idx = *start_idx;
b_idx = *start_idx;

   while ( a_idx < asz && b_idx < bsz ) {
      
      //printf("a_idx:%d b_idx%d  | %c %c  \n",a_idx,b_idx, (char)a[a_idx],(char) b[b_idx]); 
      if (a[a_idx] < b[b_idx]) { return -1; }
      else if (a[a_idx] > b[b_idx]) { return 1; }
      
      a_idx++;
      b_idx++;

   }
  if (  bsz > asz ) { return -1; }
  else if(  bsz < asz) { return 1; }
  else { return 0; }

  return 0;
}



extern int 
print_pointer ( char* pointer, size_t psz, void* func) {
    return snprintf(pointer, psz, "pointer: %p", (void*)func);    
  } 

    



int main()
{
char a[] = "xxabc";
char b[] = "xxabcd";
size_t offset = 2; 
int r = compare_function( a, sizeof(a), b, sizeof(b), (void*)&offset );







printf("result %d \n",r);

return 0;
}
