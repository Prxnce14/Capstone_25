<template>
    <div :class="pageSpecificClass">
        <footer>
            <div class="foot">
                <p>Copyright &copy {{ year }} Pelican Eats, Inc All rights reserved.</p>
            </div>
        </footer>
    </div>
</template>
  

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style>
/* Add any component specific styles here */

.foot
{
  text-align: center;
}

</style>