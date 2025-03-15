<template>
  <div v-if="isFetchingUserInfo" class="profile__loader-container">
    <Loader :size="100" />
  </div>
  <div v-if="!isFetchingUserInfo" class="profile">
    <div class="profile__details">
      <div class="profile__avatar-container">
        <component
          :is="svgComponents['PersonIcon']"
          v-if="!userInfo?.avatar && isVueComponent(svgComponents['PersonIcon'])"
          class="profile__avatar-icon"
        />
        <img
          v-if="Boolean(userInfo?.avatar)"
          :src="userInfo?.avatar"
          alt="User Avatar."
          class="profile__avatar"
        />
      </div>
      <div class="profile__person-details">
        <span :class="['profile__detail', 'profile__detail_username']">{{
          userInfo?.username
        }}</span>
        <span :class="['profile__detail', 'profile__detail_email']">{{ userInfo?.email }}</span>
        <div v-if="Boolean(userInfo?.intra_id)" class="profile__intra-container">
          <span class="profile__person-details-title">{{
            t('menu.items.item.profile.intra_id')
          }}</span>
          <span :class="['profile__detail', 'profile__detail_intra-id']">{{
            userInfo?.intra_id
          }}</span>
        </div>
      </div>
    </div>
    <MyButton
      class-name="profile__button"
      type="button"
      color="secondary"
      :loading="isLoading"
      @click="handleSignOut"
      >{{ t('auth.signout.title') }}</MyButton
    >
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import usersApi from 'entities/Users/api';
import authApi from 'shared/api/Auth';
import { Loader } from 'shared/components';
import { useMutation, useQuery } from 'shared/composables';
import { isVueComponent, svgComponents } from 'shared/lib';
import { auth } from 'store/auth.js';
import { inject } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();
const showErrorModal = inject('showErrorModal');
const notify = inject('notify');

const { data: userInfo = {}, isLoading: isFetchingUserInfo } = useQuery(usersApi.getUserInfo, {
  select: (res) => res?.data,
  onError: (error) => {
    const errorMessage =
      error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
    showErrorModal(error.status, errorMessage);
  },
});

const { mutate: onSignOut, isLoading } = useMutation(authApi.signOut, {
  onSuccess: () => {
    auth.logout();
    notify(t('success', 'success'));
    router.push('/signin');
  },
  onError: (error) => {
    const errorMessage =
      error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
    showErrorModal(error.status, errorMessage);
  },
});

const handleSignOut = () => {
  onSignOut();
};
</script>

<style scoped>
.profile {
  display: flex;
  flex-direction: column;
  row-gap: var(--big-space);

  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.profile__loader-container {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}

.profile__details {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  align-items: flex-start;

  width: 100%;
  min-width: 1px;
}

.profile__avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 90px;
  min-width: 90px;
  height: 90px;
  min-height: 90px;

  background-color: var(--light-color);
  border-radius: 50%;
}

.profile__avatar-icon {
  transform: translate(-1px, -1px);
}

.profile__avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.profile__person-details {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);
  width: 100%;
}

.profile__person-details-title {
  justify-self: flex-end;
  font-size: 0.85rem;
  color: var(--light-color-opacity-70);
  white-space: nowrap;
}

.profile__detail {
  overflow: hidden;
  width: 100%;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile__detail_username {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--secondary-color);
}

.profile__intra-container {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  width: 100%;
}

.profile__detail_intra-id {
  font-size: 0.9rem;
  color: var(--light-color-opacity-90);
}

::v-deep(.profile__button) {
  max-height: 44px;
}
</style>
